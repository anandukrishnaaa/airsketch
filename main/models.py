from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=24)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session


class Gallery(models.Model):
    gallery = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    stencil_data = models.JSONField()
    image_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApiUsageLog(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    google_api_calls = models.IntegerField(null=True, default=0)
    unsplash_api_calls = models.IntegerField(null=True, default=0)
    pexels_api_calls = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
