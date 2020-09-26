from django.shortcuts import render
from django_celery_results.models import TaskResult
from Twitter.FrontEnd_Twitter.forms import Login as loginForm
from Twitter.FrontEnd_Twitter.forms import Register as registerForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,HttpResponseRedirect
from djangoWebsite import settings
from django.contrib.messages import error
from django.contrib.auth.models import User,Permission
from .models import UserExtensionModel
from django.contrib.auth.hashers import make_password

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
            user = User.objects.get(username = username)
            authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return redirect('%s?next=%s' % (settings.LOGIN_REDIRECT_URL, request.path))
                else:
                #ActualUser.user_permissions.set('django_celery_results.view_task_results')
                    UserModel = UserExtensionModel.objects.get(user = user)
                    return redirect('%s?next=%s' % (settings.LOGIN_REDIRECT_URL, request.path))
    context = {
        'Loginform': LoginForm,
    }
    return  render(request,loginHTML,context)

def logout_page(request):
    logout(request)
    logoutHTML = 'registration/logout.html'
    return render(request,logoutHTML)

def registration_page(request):
    registrationForm = registerForm()

    registerHTML = 'registration/register.html'

    if request.method == 'POST':
        registrationForm = registerForm(request.POST)
        if registrationForm.is_valid():
            username = registrationForm.cleaned_data['username']
            password = registrationForm.cleaned_data['password']
            first_name = registrationForm.cleaned_data['first_name']
            last_name = registrationForm.cleaned_data['last_name']

            permission = Permission.objects.get(name='Can view task result')
            User.objects.create(
                    username = username,
                    password = make_password(password),
                    is_superuser = False,
                    first_name = first_name,
                    last_name = last_name,
                    is_staff = True,
            ).save()
            user = authenticate(username = username, password = password)
            userModel = User.objects.get(username = username)
            userModel.user_permissions.add(permission)
            userModel.save()
            UserExtensionModel(
                user = userModel,
                arrayTasksCompleted = [],
            ).save()
            login(request,userModel)
            return redirect('/')
    context = {
        'registerForm': registrationForm,
    }        
    return render(request,registerHTML,context)

