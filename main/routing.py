# airsketch/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/canvas/(?P<uuid>[\w-]+)$", consumers.CanvasConsumer.as_asgi()),
    re_path(r"ws/stencil/(?P<uuid>[\w-]+)$", consumers.StencilConsumer.as_asgi()),
]
