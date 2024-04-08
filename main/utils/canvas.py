import json
import aiohttp
from ._helper import log_api_usage


async def decode_canvas(event):
    try:
        # Extract data from the event
        shapes = event["shapes"]
        canvasWidth = event["canvasWidth"]
        canvasHeight = event["canvasHeight"]

        # Define the external API endpoint
        API_ENDPOINT = "https://inputtools.google.com/request?ime=handwriting&app=autodraw&dbg=1&cs=1&oe=UTF-8"

        # Prepare the request body for the external API
        requestBody = {
            "input_type": 0,
            "requests": [
                {
                    "language": "autodraw",
                    "writing_guide": {"width": canvasWidth, "height": canvasHeight},
                    "ink": shapes,
                }
            ],
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(API_ENDPOINT, json=requestBody) as response:
                response_data = await response.json()

                # Check if the response is successful
                if response.status == 200:
                    # Process the response data
                    if (
                        len(response_data) > 1
                        and len(response_data[1]) > 0
                        and "debug_info" in response_data[1][0][3]
                    ):
                        suggestions = (
                            response_data[1][0][3]["debug_info"]
                            .split("SCORESINKS: ")[1]
                            .split(" Service_Recognize:")[0]
                        )

                        # Increment the Google API usage log
                        await log_api_usage(google_api_calls=1)

                        return {
                            "statusCode": 200,
                            "headers": {"Content-Type": "application/json"},
                            "body": json.dumps({"data": suggestions}),
                        }
                    else:
                        raise ValueError(
                            "Unexpected response structure from the external API"
                        )
                else:
                    raise aiohttp.ClientResponseError(
                        response.request_info, response.history, code=response.status
                    )

    except Exception as error:
        print("Error processing request:", error)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(error)}),
        }
