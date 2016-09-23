from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('mainapp/index.html')
    return HttpResponse(template.render(request))

def test(request):
    template = loader.get_template('mainapp/test.html')
    return HttpResponse(template.render(request))
