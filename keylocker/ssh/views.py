from ssh.models import SSHKey
from django.http import HttpResponse
from django.db.models import Q

"""
Examples:

/ssh/d81eaef9837277a91b2a6109a6cd695d97933f18@oix-ficam-loa1
/ssh/d81eaef9837277a91b2a6109a6cd695d97933f18@something-i-defined-myself
/ssh/89565e416cd382ecc05bd07d7367c143347ca35a@swamid-al2

"""

def get_in_authorized_key_fmt(request,utag,labels=None):
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
