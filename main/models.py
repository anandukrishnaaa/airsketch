from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=24)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
