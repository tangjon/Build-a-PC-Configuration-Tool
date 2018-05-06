from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'home.html', {'title': 'Home'})


def login(request):
    return render(request, 'login.html', {'title': 'Login'})