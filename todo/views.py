from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.db import IntegrityError
# Create your views here.
def Home(request):
    return render(request,'todo/home.html')

def LogOut(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
        
def SignUp(request):
    if(request.method == 'GET'):
        return render(request, 'todo/signup.html', {"form": UserCreationForm()})
    else:
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('current_todos') 
            except IntegrityError:
                return render(request, 'todo/signup.html', {"form": UserCreationForm(), 'error': "Username has been taken!"})

        else:
            return render(request, 'todo/signup.html', {"form": UserCreationForm(), 'error': "Password did not Match!"})


def CurrentTodos(request):
    return render(request,"todo/todo.html")