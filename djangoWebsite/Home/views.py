from django.shortcuts import render
from django_celery_results.models import TaskResult
from Twitter.FrontEnd_Twitter.forms import Login as loginForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from djangoWebsite import settings




# Create your views here.

def home_page(request):
    homeHTML = 'registration/index.html'
    return render(request,homeHTML)

def login_page(request):
    loginHTML = 'registration/login.html'

    LoginForm = loginForm()

    if request.method == 'POST':
        LoginForm = loginForm(request.POST)
        if LoginForm.is_valid():
            username = LoginForm.cleaned_data['username']
            password = LoginForm.cleaned_data['password']
            user = authenticate(username = username , password = password)

            if user is not None:
                login(request,user)
                return redirect('%s?next=%s' % (settings.LOGIN_REDIRECT_URL, request.path))
            else:
                pass

    context = {
        'Loginform': LoginForm,
        "numTasks": TaskResult.objects.all().count()
    }
    print("THIS PAGE")
    return  render(request,loginHTML,context)

def logout_page(request):
    logout(request)
    logoutHTML = 'registration/logout.html'
    return render(request,logoutHTML)
