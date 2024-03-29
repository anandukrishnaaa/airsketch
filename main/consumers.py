from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils.canvas import decode_canvas


class CanvasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            # Parse incoming JSON data
            data = json.loads(text_data)

            # Call the decode_canvas function with the parsed data
            result = await decode_canvas(data)

            # Serialize result to JSON string
            result_json = json.dumps(result)

            # Send JSON response
            await self.send(result_json)
        except Exception as e:
            # Return error response if any exception occurs
            error_message = {"error": str(e)}
            await self.send(json.dumps(error_message))

    async def disconnect(self, close_code):
        pass  # You can add disconnect handling if needed
