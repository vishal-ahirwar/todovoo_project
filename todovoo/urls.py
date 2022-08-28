
from django.contrib import admin
from django.urls import path, include
from todo.views import SignUp, CurrentTodos, Home, LogOut, LogIn, Create
app_name = "todo"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', SignUp, name='sign_up'),
    path('logout', LogOut, name='logout'),
    # todovoo
    path('current-todos/', CurrentTodos, name='current_todos'),
    path('', Home, name="home"),
    path('login',LogIn,name="log_in"),
    path('create',Create,name="create"),
]
