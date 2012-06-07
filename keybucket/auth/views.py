from django.template.response import TemplateResponse

__author__ = 'leifj'

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site

from saml2 import BINDING_HTTP_REDIRECT
from saml2.client import Saml2Client

from djangosaml2.cache import OutstandingQueriesCache
from djangosaml2.conf import get_config_loader
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect
from urlparse import urlparse

import logging
logger = logging.getLogger('djangosaml2')

def get_custom_setting(name, default=None):
    if hasattr(settings, name):
        return getattr(settings, name)
    else:
        return default


DEFAULT_CONFIG_LOADER = get_custom_setting(
    'SAML_CONFIG_LOADER',
    'djangosaml2.conf.config_settings_loader',
    )

IDP_COOKIE="_djangosaml2_idp"

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request,
          config_loader=DEFAULT_CONFIG_LOADER,
          redirect_field_name=REDIRECT_FIELD_NAME,
          template_name='auth/login.html',
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None,
          authorization_error_template='djangosaml2/auth_error.html'):
    """SAML Authorization Request initiator

    This view initiates the SAML2 Authorization handshake
    using the pysaml2 library to create the AuthnRequest.
    It uses the SAML 2.0 Http Redirect protocol binding.
    """

    logger.debug('Login process started')
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == 'POST':
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)

    request.session.set_test_cookie()
    selected_idp = request.GET.get('idp', None)
    conf = get_config_loader(config_loader, request)
    came_from = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    last_selected_idp = request.COOKIES.get(IDP_COOKIE,None)

    if last_selected_idp:
        print conf.metadata.entity[last_selected_idp]

    if selected_idp:
        print conf.metadata.entity[selected_idp]
        # is a embedded wayf needed?
        client = Saml2Client(conf, logger=logger)
        try:
            (session_id, result) = client.authenticate(
                entityid=selected_idp, relay_state=came_from,
                binding=BINDING_HTTP_REDIRECT,
            )
        except TypeError, e:
            logger.error('Unable to know which IdP to use')
            return HttpResponse(unicode(e))

        assert len(result) == 2
        assert result[0] == 'Location'
        location = result[1]

        logger.debug('Saving the session_id in the OutstandingQueries cache')
        oq_cache = OutstandingQueriesCache(request.session)
        oq_cache.set(session_id, came_from)

        logger.debug('Redirecting the user to the IdP')
        response = HttpResponseRedirect(location)
        response.set_cookie(IDP_COOKIE,selected_idp)
        return response
    else:
        form = authentication_form(request)
        idp_set = conf.idps()
        idps = []
        if idp_set:
            idps.extend(idp_set.items())
        current_site = get_current_site(request)
        context = {
            'available_idps': idps,
            'last_selected_idp': last_selected_idp,
            'came_from': came_from,
            'form': form,
            redirect_field_name: redirect_to,
            'site': current_site,
            'site_name': current_site.name,
        }
        if extra_context is not None:
            context.update(extra_context)
        return TemplateResponse(request, template_name, context, current_app=current_app)


