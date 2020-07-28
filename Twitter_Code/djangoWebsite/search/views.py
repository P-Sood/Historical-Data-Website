from django.shortcuts import render
from django.http import HttpResponse


# IT would take so much time to actually make an html page 
# We use something named templates

def home(request):
    return HttpResponse('<h1> Search Page </h1>')

def tips(request):
    return HttpResponse('<h2> Tips and Tricks </h2>')

# Create your views here.
