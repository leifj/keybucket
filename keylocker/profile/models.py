from django.db import models
from django.contrib.auth.models import User
from django.db import fields

class SSHKey(models.Model):
    user = models.ForeignKey(User)
    idp = models.CharField(max_length=256)
