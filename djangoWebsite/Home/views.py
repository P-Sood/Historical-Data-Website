from django.shortcuts import render

# Create your views here.

def home(request):
    homeHTML = 'registration/index.html'
    context = {
        "numTasks": 5
    }
    return render(request,homeHTML,context)
