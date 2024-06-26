from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("playground/<uuid:uuid>/", views.playground, name="playground"),
    path(
        "gallery/<uuid:uuid>/", views.gallery, name="gallery"
    ),  # URL pattern for playground.html with UUID parameter
]
