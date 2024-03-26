# main/views.py

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from . import models
from . import forms
import json
from .utils.canvas import decode_canvas


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
    response.set_cookie("username", user.username)
    response.set_cookie("is_author", True)
    response.set_cookie("is_editable", True)
    return response


def canvas(request):
    if request.method == "POST":
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)

            # Call the decode_canvas function with the parsed data
            result = decode_canvas(data)

            # Return JSON response
            return JsonResponse(result)
        except Exception as e:
            # Return error response if any exception occurs
            return JsonResponse({"error": str(e)}, status=500)

    # Return error response if request method is not POST
    return JsonResponse({"error": "Method not allowed"}, status=405)
