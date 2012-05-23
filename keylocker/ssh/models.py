from django.db import models
from django.contrib.auth.models import User
from django.db import fields

class SSHKey(models.Model):
    name = fields.CharField(max_length=128)
    key = fields.TextField()
    user = models.ForeignKey(User)
    description = fields.TextField(null=True,blank=True)
