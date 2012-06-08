# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def welcome(request):
    return about(request,"welcome")

def about(request,id):
    return render_to_response('profile/%s.html' % id,{},RequestContext(request))