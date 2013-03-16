from django.http import HttpResponse
from django.shortcuts import render
from random import randint

def home(request):
    return render(request, 'home/index.html', {'r': str(request)})


def ping(request):
    return HttpResponse('200')


def pong(request):
    for a in range(1, 9000):
        primes(randint(0, 9999))
        a.__sizeof__()
    return HttpResponse(primes(randint(1, 10)))


def primes(n):
    if n==2:
        return [2]
    elif n<2:
        return []
    s=range(3,n+1,2)
    mroot = n ** 0.5
    half=(n+1)/2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)/2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]
