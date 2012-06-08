from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from profile.views import welcome

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'keybucket.views.home', name='home'),
    # url(r'^keybucket/', include('keybucket.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^/?$','keybucket.profile.views.welcome'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ssh/',include('keybucket.ssh.urls')),
    url(r'^saml2/sp/',include('djangosaml2.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^auth/',include('keybucket.auth.urls')),
    url(r'^about/(?P<id>.+)/?$',"keybucket.profile.views.about"),
    url(r'^site-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/static' % settings.BASE_DIR, 'show_indexes': True}),
)
