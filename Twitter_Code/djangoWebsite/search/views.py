from django.shortcuts import render

posts = [
    {
        ''
    }
]

# IT would take so much time to actually make an html page 
# We use something named templates

def home(request):
    return render(request,'search/home.html')

def tips(request):
    return render(request,'search/tips.html')

