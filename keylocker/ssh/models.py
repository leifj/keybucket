from django.db import models
from django.contrib.auth.models import User
from assurance.models import Assurance

class SSHKey(models.Model):
    user = models.ForeignKey(User,editable=False)
    assurance = models.ForeignKey(Assurance)
    name = models.SlugField(max_length=128,unique=False)
    key = models.TextField()
    description = models.TextField(null=True,blank=True)
    verified = models.BooleanField(default=False)
    timecreated = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    lastverified = models.DateTimeField(null=True,blank=True)
    
    def __unicode__(self):
        return "%s %s+%s" % (self.key,self.name,self.assurance)