'''
Created on May 28, 2012

@author: leifj
'''
from django.forms.models import ModelForm
from ssh.models import SSHKey

class SSHKeyForm(ModelForm):
    class Meta:
        model = SSHKey
        
