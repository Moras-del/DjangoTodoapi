from django.urls import path
from rest_framework.authtoken import views

from .views import TodoTaskList, UserRegistration

urlpatterns = [
    path('todotasks', TodoTaskList.as_view()),
    path('todotasks/<int:pk>', TodoTaskList.as_view()),
    path('auth', views.obtain_auth_token),
    path('register', UserRegistration.as_view())
]
