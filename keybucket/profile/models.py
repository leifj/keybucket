import hashlib
from django.dispatch.dispatcher import receiver
import os
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import User
from keybucket.assurance.models import Assurance, IdentityProvider
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models.signals import post_save

def get_custom_setting(name, default=None):
    if hasattr(settings, name):
        return getattr(settings, name)
    else:
        return default

class UserProfile(models.Model):
    user = models.ForeignKey(User,related_name="profile")
    display_name = models.CharField(max_length=256)
    idp = models.CharField(max_length=256)
    uhash = models.CharField(max_length=256,unique=True) # sha1 of user.username
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Profile for %s" % self.user

def populate_profile(sender, user, request, **kwargs):
    """
    Check if profile exists when user logs in, otherwise create it.
    Also populates idp from the request.
    """
    modified = False
    profile,created = UserProfile.objects.get_or_create(user=user)
    if not profile.uhash:
        profile.uhash = hashlib.sha1(user.username).hexdigest()
        modified = True
    
    #ToDo get idp from request and set
    idp = request.META.get('Shib_Identity_Provider',None)
    if idp is not None:
        profile.idp = idp
        modified = True

        #auto-populate idp table
        idp_object,created = IdentityProvider.objects.get_or_create(uri=idp)

    if modified:
        profile.save()
    
    levels = []
    authn_context_class = request.META.get('Shib_AuthnContext_Class',None)
    if authn_context_class is not None:
        for uri in authn_context_class.split():
            try:
                level = Assurance.objects.get(uri=uri,assignable=False) #only look for "real" LoAs
                levels.append(level)
            except ObjectDoesNotExist:
                pass
    
    if levels is None and idp is not None:
        # fall back to default for the IdP if exists
        try:
            identity_provider = IdentityProvider.objects.get_or_create(uri=idp)
            if identity_provider.default_assurance != None:
                levels.append(identity_provider.default_assurance)
        except ObjectDoesNotExist:
            pass

    if user.username in get_custom_setting('AUTO_REMOTE_SUPERUSERS',[]):
        user.is_superuser = True
        user.is_staff = True
        user.password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        with open("/tmp/%s" % user.username,'w') as pwf:
            pwf.write(user.password)
        os.chmod("/tmp/%s" % user.username,0600)
        user.save()
    
    request.session['assurance_levels'] = levels
    return

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    profile,created = UserProfile.objects.get_or_create(user=instance)

user_logged_in.connect(populate_profile)

def assurance_levels(request):
    try:
        request.session['assurance_levels']
    except KeyError:
        request.session['assurance_levels'] = []

    return request.session['assurance_levels']
