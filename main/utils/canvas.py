import json
import requests


def decode_canvas(event):
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

        # Make the request to the external API
        response = requests.post(
            API_ENDPOINT,
            headers={"Content-Type": "application/json; charset=utf-8"},
            data=json.dumps(requestBody),
        )

        print(response.json())

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()

            # Ensure the response structure is as expected before processing
            if len(data) > 1 and len(data[1]) > 0 and "debug_info" in data[1][0][3]:
                suggestions = (
                    data[1][0][3]["debug_info"]
                    .split("SCORESINKS: ")[1]
                    .split(" Service_Recognize:")[0]
                )

                # Return the suggestions
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"data": suggestions}),
                }
            else:
                raise ValueError("Unexpected response structure from the external API")
        else:
            raise requests.HTTPError(f"HTTP Error: {response.status_code}")

    except Exception as error:
        print("Error processing request:", error)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(error)}),
        }
