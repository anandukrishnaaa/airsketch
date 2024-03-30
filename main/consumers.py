from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils.canvas import decode_canvas
from .utils.stencil import fetch_stencil


class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Add logic if needed


class CanvasConsumer(BaseConsumer):
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            result = await decode_canvas(data)
            result_json = json.dumps(result)
            await self.send(result_json)
        except json.JSONDecodeError as e:
            error_message = {"error": "Invalid JSON format"}
            await self.send(json.dumps(error_message))
        except Exception as e:
            error_message = {"error": str(e)}
            await self.send(json.dumps(error_message))


import json


class StencilConsumer(BaseConsumer):
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            stencil_data = await fetch_stencil(data)
            # Convert stencil_data to a JSON string before sending
            await self.send(json.dumps(stencil_data))
        except json.JSONDecodeError as e:
            error_message = {"error": "Invalid JSON format"}
            await self.send(json.dumps(error_message))
        except Exception as e:
            error_message = {"error": str(e)}
            await self.send(json.dumps(error_message))
