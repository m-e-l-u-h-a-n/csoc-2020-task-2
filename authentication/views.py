from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.http import HttpResponse
# @csrf_exempt
def loginView(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST['Username']
        password =  request.POST['Password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'templates/login.html',{'message':"Invalid Credentials"})
    else:
        return render(request, 'login.html',{'msg':"Invalid request method"})
def logoutView(request):
    logout(request)
    return redirect('index')

def registerView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Invalid credentials!')
    else:
        return render(request, 'templates/signup.html', {'form':SignUpForm(), 'error':'Bad Request'})

