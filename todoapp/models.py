from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated


class AuthenticatedManager(models.Manager):
    def get_by_id(self, pk, user):
        todo = super().get_queryset().get(pk=pk)
        if todo.owner == user:
            return todo
        else:
            raise NotAuthenticated()


class TodoTask(models.Model):
    description = models.CharField(max_length=100)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    authenticated = AuthenticatedManager()
    objects = models.Manager()
    def __str__(self):
        return self.description

    class Meta:
        ordering = ('date_end',)


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
