
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
# Create your views here.


def Home(request):
    todo=Todo.objects.filter(creator=request.user)
    return render(request, "todo/home.html",{"todos":todo})

def Create(request):
    if request.method=="GET":
        return render(request,"todo/create.html",{"error":"Get Request ..."})
    else:
        try:
            form=TodoForm(request.POST)
            form.save(commit=False)
            form.creator=request.user
            form.save()
            return redirect("current_todos")
        except ValueError:
            return render(request,"todo/create.html",{"error":"Bad Data Passed in. Please Try Again!"})
            

def LogIn(request):
    if request.method == "GET":
        return render(request, "todo/login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "todo/login.html", {"form": AuthenticationForm, "error": "Username or Password Incorrect!"})


def LogOut(request):
    if request.method == 'POST':
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
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {"form": UserCreationForm(), 'error': "Username has been taken!"})

        else:
            return render(request, 'todo/signup.html', {"form": UserCreationForm(), 'error': "Password did not Match!"})


def CurrentTodos(request):
    todo=Todo.objects.filter(creator=request.user)
    return render(request, "todo/todo.html",{"todos":todo})
