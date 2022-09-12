from rest_framework import generics,permissions
from .serializers import TodoSerializer,TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.db import IntegrityError

@csrf_exempt
def signup(request):
    if request.method=="POST":
        try:
            data=JSONParser.parse(request)
            user=User.objects.create_user(data['username'],data['password'])
            user.save()
            return JsonResponse({'token':'Account Creation Done!'},status=201)
        except IntegrityError:
            return JsonResponse({'error':'username has been already taken !please try Again!'},status=400)



class TodoList(generics.ListAPIView):
    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(creator=user)

class TodoCreate(generics.ListCreateAPIView):
    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(creator=user)
    def perform_create(self,serializer):
        serializer.save(creator=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(creator=user)
    def perform_create(self,serializer):
        serializer.save(creator=self.request.user)

class TodoComplete(generics.UpdateAPIView):
    serializer_class=TodoCompleteSerializer
    permission_classed=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(creator=user)

    def perform_update(self,serializer):
        serializer.instance.datecompleted=timezone.now()
        serializer.save()
