
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def DeleteToDo(request, todo_pk):
    if(request.method == "POST"):
        todo = get_object_or_404(Todo, pk=todo_pk, creator=request.user)
        todo.delete()
        return redirect("home")


def CompleteToDo(request, todo_pk):
    if (request.method == "POST"):
        todo = get_object_or_404(Todo, pk=todo_pk, creator=request.user)
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect("home")


@login_required
def ViewToDo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, creator=request.user)
    if (request.method == "GET"):
        form = TodoForm(instance=todo)
        return render(request, "todo/view-todo.html", {"title": todo.title, "id": todo.id, "form": form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect("home")
        except:
            return render(request, "todo/view-todo.html", {"title": todo.title, "form": form, "error": "Caught Unknown Error !"})


@login_required
def Home(request):
    try:
        todo = Todo.objects.filter(creator=request.user)
    except TypeError:
        todo = []
    if (request.method == 'POST'):
        try:
            form = TodoForm(request.POST)
            new_form = form.save(commit=False)
            new_form.creator = request.user
            new_form.save()
            return render(request, "todo/home.html", {"error": "+1 Todo has been Added", "form": TodoForm(), "todos": todo})
        except:
            return render(request, "todo/home.html", {"error": "Unknown Error Caught!", "todos": todo, "form": TodoForm()})
    else:
        return render(request, "todo/home.html", {"todos": todo, "form": TodoForm()})


@login_required
def Create(request):
    if (request.method == "GET"):
        return render(request, "todo/create.html", {"error": "Get Request ...", "form": TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_form = form.save(commit=False)
            new_form.creator = request.user
            new_form.save()
            return redirect("current_todos")
        except ValueError:
            return render(request, "todo/create.html", {"error": "Bad Data Passed in. Please Try Again!"})


def LogIn(request):
    if (request.method == "GET"):
        return render(request, "todo/login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST["password"])
        if (user is not None):
            login(request, user)
            return redirect('home')
        else:
            return render(request, "todo/login.html", {"form": AuthenticationForm, "error": "Username or Password Incorrect!"})


@login_required
def LogOut(request):
    if (request.method == 'POST'):
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


@login_required
def CurrentTodos(request):
    todo = Todo.objects.filter(creator=request.user)
    return render(request, "todo/todo.html", {"todos": todo})
