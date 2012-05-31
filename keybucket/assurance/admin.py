from django.contrib import admin
from keybucket.assurance.models import IdentityProvider
from keybucket.assurance.models import Assurance

admin.site.register(Assurance)
admin.site.register(IdentityProvider)
