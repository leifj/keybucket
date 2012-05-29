# Create your views here.
from ssh.forms import SSHKeyForm
from django.http import HttpResponseRedirect
from ssh.models import SSHKey
from assurance.models import Assurance
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from profile.models import assurance_levels

def add_key(request):
    if request.method == 'POST':
        form = SSHKeyForm(request.POST)
        levels = assurance_levels(request)
        levels.extend(Assurance.objects.filter(assignable=True))
        form.fields['assurance'].choices=[(al.id,al.name) for al in levels]
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/ssh")
    
    sk = SSHKey(user=request.user)
    form = SSHKeyForm(instance=sk)
    levels = assurance_levels(request)
    levels.extend(Assurance.objects.filter(assignable=True))
    form.fields['assurance'].choices=[(al.id,al.name) for al in levels]
    
    return render_to_response('ssh/add.html',{'form':form,'user':request.user},RequestContext(request))

