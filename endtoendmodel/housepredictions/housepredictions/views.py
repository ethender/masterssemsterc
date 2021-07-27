from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse


def home(request):
    return render(request,'Home.html')