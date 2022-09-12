from rest_framework import generics,permissions
from .serializers import TodoSerializer
from todo.models import Todo
class TodoList(generics.ListAPIView):
    serializer_class=TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(creator=user)
