from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User,related="profile")
    idp = models.CharField(max_length=256)
    uhash = models.CharField(max_length=256,unique=True) # sha1 of user.username
