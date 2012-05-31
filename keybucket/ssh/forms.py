'''
Created on May 28, 2012

@author: leifj
'''
from django.forms.models import ModelForm
from keybucket.ssh.models import SSHKey
from django import forms
from keybucket.assurance.models import Assurance
from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple

class SSHKeyForm(ModelForm):
    class Meta:
        model = SSHKey
        fields = ('name', 'description', 'assurance', 'key')
        #widgets = {'assurance': CheckboxSelectMultiple}

