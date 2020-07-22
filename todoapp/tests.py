import json

from django.test import TestCase
from .models import TodoTask
from .views import TodoTaskList
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate
import datetime


class TodosTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user", None, "haslo")
        TodoTask.objects.create(pk=1, description="opis", date_end=datetime.datetime.now(), owner_id=self.user.id)

    def test_end_date(self):
        todo = TodoTask.objects.get(pk=1)
        self.assertIsNotNone(todo.date_start)

    def test_token_creation(self):
        token = Token.objects.get(user=self.user)
        self.assertIsNotNone(token)

    def test_description(self):
        desc = TodoTask.objects.get(pk=1).description
        self.assertEquals(desc, "opis")

class ApiTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("user", None, "haslo")
        self.user_token = Token.objects.get(user=self.user)
        self.factory = APIRequestFactory()
        for i in range(5):
            TodoTask.objects.create(pk=i,
                                    description="task_nr_{}".format(i),
                                    date_end=datetime.datetime.now(),
                                    owner_id=self.user.id)

    def test_get_todos(self):
        request = self.factory.get("/todotasks")
        force_authenticate(request, self.user)
        response = TodoTaskList.as_view()(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 5)

    def test_post_todo(self):
        request_body = {"description": "new task", "date_end": str(datetime.datetime.now())}
        request = self.factory.post("/todotasks", json.dumps(request_body), content_type="application/json")
        force_authenticate(request, self.user)
        response = TodoTaskList.as_view()(request)
        new_todo = response.data[-1]
        self.assertEquals(new_todo['description'], 'new task')
        self.assertEquals(response.status_code, 201)

    def test_delete_todo(self):
        request = self.factory.delete("/todotasks/1")
        force_authenticate(request, self.user)
        response = TodoTaskList.as_view()(request, 1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 4)

    def test_unauthorized_delete_todo(self):
        new_user = User.objects.create_user("new_user", None, "password")
        request = self.factory.delete("/todotasks/1")
        force_authenticate(request, new_user)
        response = TodoTaskList.as_view()(request, 1)
        self.assertEquals(response.status_code, 401)
