from django.urls import path
from . import views

urlpatterns=[
    path('todos/',views.TodoCreate.as_view(),name='completed'),
    path('todos/<int:pk>/',views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete/',views.TodoComplete.as_view()),
    path('signup',views.signup,name='signup'),
]
