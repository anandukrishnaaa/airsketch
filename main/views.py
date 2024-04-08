# main/views.py

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from . import models
from . import forms
import json


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.uuid = uuid.uuid4()  # Generating UUID for the user
            user.save()

            # Create a Session object and associate it with the user
            session = models.Session.objects.create(user=user, session=str(user.uuid))

            # Redirect to playground.html with the UUID
            return redirect("playground", uuid=user.uuid)
    else:
        form = forms.UserForm()
    return render(request, "index.html", {"form": form})


def playground(request, uuid):
    # Retrieve session based on the provided UUID
    session = get_object_or_404(models.Session, session=uuid)

    # Retrieve the associated user
    user = session.user

    response = render(
        request,
        "playground.html",
        {"uuid": uuid, "username": user.username, "email": user.email},
    )
    return response


def gallery(request, uuid=None):
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("uuid")  # Assuming uuid is sent in the request
        stencil_data = data.get("allItems")
        image_data = data.get("imageData")

        # Fetch the session using the UUID
        session = models.Session.objects.get(session=session_id)
        user = session.user  # Get the user associated with the session

        try:
            # Check if a gallery with the given UUID already exists
            gallery = models.Gallery.objects.get(gallery=session_id)
            # If exists, update the existing gallery
            gallery.stencil_data = stencil_data
            gallery.image_data = image_data
            gallery.save()
            # Return a JSON response indicating success
            return JsonResponse(
                {
                    "success": True,
                    "message": "Gallery updated! Redirecting in 5 seconds.",
                }
            )
        except models.Gallery.DoesNotExist:
            # If the gallery doesn't exist, create a new one
            models.Gallery.objects.create(
                gallery=session_id,
                user=user,
                session=session,
                stencil_data=stencil_data,
                image_data=image_data,
            )
            # Return a JSON response indicating success
            return JsonResponse(
                {
                    "success": True,
                    "message": "Gallery created! Redirecting in 5 seconds.",
                }
            )
    elif uuid:
        # Assuming uuid is provided in the URL
        try:
            # Fetch the gallery data for the given uuid
            gallery = models.Gallery.objects.get(gallery=uuid)
            # Get related user's username
            username = gallery.user.username
            # Get stencil_data and image_data
            stencil_data = gallery.stencil_data
            image_data = gallery.image_data
            # Create context with the retrieved data
            context = {
                "username": username,
                "stencil_data": stencil_data,
                "image_data": image_data,
            }
            return render(request, "gallery.html", context)
        except models.Gallery.DoesNotExist:
            return JsonResponse({"success": False, "error": "Gallery not found"})
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method or UUID not provided"}
        )
