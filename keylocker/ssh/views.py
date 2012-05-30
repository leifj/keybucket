from ssh.models import SSHKey
from django.http import HttpResponse
from django.db.models import Q
from ssh.forms import SSHKeyForm
from django.http import HttpResponseRedirect
from ssh.models import SSHKey
from assurance.models import Assurance
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from profile.models import assurance_levels

"""
Examples:

/ssh/d81eaef9837277a91b2a6109a6cd695d97933f18@oix-ficam-loa1
/ssh/d81eaef9837277a91b2a6109a6cd695d97933f18@something-i-defined-myself
/ssh/89565e416cd382ecc05bd07d7367c143347ca35a@swamid-al2

"""

def get_in_authorized_keys_fmt(request,utag,labels=None):
    keys = None
    if '@' in utag:
        (uhash,level) = utag.split('@')
        keys = SSHKey.objects.filter(Q(user__profile__utag=uhash) & Q(assurance__name=level))
    else:
        keys = SSHKey.objects.filter(user__profile__utag=utag)
    o = []
    for key in keys:
        o.append("%s %s+%s" % (key.key,key.name,key.assurance))
    return HttpResponse("\n".join(o))

@login_required
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

@login_required
def list_keys(request):
    qs = SSHKey.objects.filter(user=request.user)
    return render_to_response('ssh/list.html',{'keys': qs})