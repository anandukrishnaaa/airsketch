# main/views.py

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from . import models
from . import forms


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

    return render(
        request,
        "playground.html",
        {"uuid": uuid, "username": user.username, "email": user.email},
    )


def canvas(request):
    if request.method == "POST":
        # Process the data
        data = {"status": "success"}
        return JsonResponse(data)
