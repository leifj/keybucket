from django.db import models
from django.contrib.auth.models import User
from assurance.models import Assurance

class SSHKey(models.Model):
    user = models.ForeignKey(User,editable=False)
    assurance = models.ForeignKey(Assurance)
    name = models.CharField(max_length=128)
    key = models.TextField()
    description = models.TextField(null=True,blank=True)