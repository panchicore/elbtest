from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html', {'r': str(request)})


def ping(request):
    return HttpResponse('200')


def pong(request):
    return HttpResponse('pong')

