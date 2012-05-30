from django.db import models
from django.contrib.auth.models import User

class Assurance(models.Model):
    owner = models.ForeignKey(User)
    assignable = models.BooleanField(default=False)
    uri = models.CharField(max_length=64,unique=True)
    name = models.CharField(max_length=64,unique=True)
    
    def __unicode__(self):
        return self.name

class IdentityProvider(models.Model):
    uri = models.CharField(max_length=64,unique=True)
    default_assurance = models.ForeignKey(Assurance,blank=True,null=True)

def assurance_by_name(n):
    return Assurance.objects.get(name=n)