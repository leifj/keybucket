from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('keybucket.auth.views',
    url(r'^login/','login_dual')
)
