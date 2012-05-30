__author__ = 'leifj'

from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from keylocker.ssh.models import SSHKey

urlpatterns = patterns('keylocker.ssh.views',
    url(r'^/?$','list_keys'),
    url(r'^add/?$','add_key'),
    url(r'^(?P<utag>[^+]+)\+(?P<labels>.+)/?$','get_in_authorized_keys_fmt'),
    url(r'^(?P<utag>[^+]+)/?$','get_in_authorized_keys_fmt'),
)