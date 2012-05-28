from ssh.models import SSHKey
from django.http import HttpResponse

def get_in_authorized_key_fmt(request,utag,labels=None):
    keys = SSHKey.objects.filter(user__profile__utag=utag)
    o = []
    for key in keys:
        o.append("%s %s" % (key.key,key.name))
    return HttpResponse("\n".join(o))
