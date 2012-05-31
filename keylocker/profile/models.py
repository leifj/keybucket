import hashlib
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import User
from assurance.models import Assurance, IdentityProvider
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(models.Model):
    user = models.ForeignKey(User,related_name="profile")
    display_name = models.CharField(max_length=256)
    idp = models.CharField(max_length=256)
    uhash = models.CharField(max_length=256,unique=True) # sha1 of user.username

def populate_profile(sender, user, request, **kwargs):
    """
    Check if profile exists when user logs in, otherwise create it.
    Also populates idp from the request.
    """
    modified = False
    profile = UserProfile.objects.get_or_create(user=user)
    if not profile.uhash:
        profile.uhash = hashlib.sha1(user.username).hexdigest()
        modified = True
    
    #ToDo get idp from request and set
    idp = request.META.get('Shib_Identity_Provider',None)
    if idp != None:
        profile.idp = idp
        modified = True
        
    if modified:
        profile.save()
    
    levels = []
    authn_context_class = request.META.get('Shib_AuthnContext_Class',None)
    if authn_context_class != None:
        for uri in authn_context_class.split():
            try:
                level = Assurance.objects.get(uri=uri,assignable=False) #only look for "real" LoAs
                levels.append(level)
            except ObjectDoesNotExist:
                pass
    
    if levels is None and idp != None:
        # fall back to default for the IdP if exists
        try:
            identity_provider = IdentityProvider.objects.get_or_create(uri=idp)
            if identity_provider.default_assurance != None:
                levels.append(identity_provider.default_assurance)
        except ObjectDoesNotExist:
            pass
    
    request.session['assurance_levels'] = levels
        
    return

user_logged_in.connect(populate_profile)

def assurance_levels(request):
    return request.session['assurance_levels']
