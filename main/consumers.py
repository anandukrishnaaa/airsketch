from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils.canvas import decode_canvas
from .utils.stencil import fetch_stencil
from .utils.image import fetch_images_by_keyword_unsplsh, fetch_images_by_keyword_pxls
from .utils._helper import extract_items


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


class ImageConsumer(BaseConsumer):
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)

            genMode = data["genMode"]
            genSrc = data["genSrc"]

            print(data)

            item_list = await extract_items(data["data"])

            print(item_list)

            print("genMode:", genMode)
            print("genSrc:", genSrc)

            if genSrc == "unsplsh":
                if genMode == "chained":
                    print("UNSPLSH Chained")
                    img_data = await fetch_images_by_keyword_unsplsh(
                        item_list, chained=True
                    )
                    # print(img_data)
                else:
                    print("UNSPLSH Single")
                    img_data = await fetch_images_by_keyword_unsplsh(
                        item_list, single=True
                    )
                    # print(img_data)
            elif genSrc == "pxls":
                if genMode == "chained":
                    print("PXLS Chained")
                    img_data = await fetch_images_by_keyword_pxls(
                        item_list, chained=True
                    )
                    # print(img_data)
                else:
                    print("PXLS Single")
                    img_data = await fetch_images_by_keyword_pxls(
                        item_list, single=True
                    )
                    # print(img_data)
            else:
                raise ValueError("Invalid config. parameters!")

            await self.send(json.dumps(img_data))
        except json.JSONDecodeError as e:
            error_message = {"error": "Invalid JSON format"}
            await self.send(json.dumps(error_message))
        except ValueError as e:
            error_message = {"error": str(e)}
            await self.send(json.dumps(error_message))
        except Exception as e:
            error_message = {"error": str(e)}
            await self.send(json.dumps(error_message))
