from django.shortcuts import render

# Create your views here.
title = 'User Page'


def view_profile(request):
    return render(request, 'profile.html', {'title': title})
