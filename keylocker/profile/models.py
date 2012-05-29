import hashlib
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User,related="profile")
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
    return

user_logged_in.connect(populate_profile)
