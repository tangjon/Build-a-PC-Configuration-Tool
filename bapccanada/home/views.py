from django.shortcuts import render
from django.http import HttpResponse


title = 'Home'


def index(request):
    return render(request, 'home.html', {'title': title})
