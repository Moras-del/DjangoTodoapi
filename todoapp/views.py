from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TodoTask
from .serializers import TodoTaskSerializer, UserSerializer


class TodoTaskList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(self.__getTasks(request.user))

    def post(self, request):
        serializer = TodoTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(self.__getTasks(request.user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        todo_task = TodoTask.authenticated.get_by_id(pk=pk, user=request.user)
        serializer = TodoTaskSerializer(todo_task, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo_task = TodoTask.authenticated.get_by_id(pk=pk, user=request.user)
        todo_task.delete()
        return Response(self.__getTasks(request.user), status=status.HTTP_200_OK)

    def __getTasks(self, user):
        tasks = TodoTask.objects.filter(owner=user)
        serializer = TodoTaskSerializer(tasks, many=True)
        return serializer.data


class UserRegistration(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"token": Token.objects.get(user=user).key}, status.HTTP_201_CREATED)
        return Response({"message": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
