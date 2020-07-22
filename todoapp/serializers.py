from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TodoTask


class TodoTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoTask
        fields = ['pk', 'description', 'date_start', 'date_end']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
