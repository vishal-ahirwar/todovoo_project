from django.urls import path
from . import views
urlpatterns=[
    path('todos/completed',views.TodoList.as_view(),name='completed'),
]
