from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def baseview(request):
    return render(request, 'home.html')

def homeview(request):
    return render(request, 'home.html')

def aboutusview(request):
    template = loader.get_template('aboutus.html')
    return HttpResponse(template.render())

def photosview(request):
    template = loader.get_template('photos.html')
    return HttpResponse(template.render())    