import json
import os
from django.conf import settings

json_path = os.path.join(settings.BASE_DIR / "main/utils/stencils.json")

# Load stencils.json into a dictionary for efficient lookup
with open(json_path, "r") as f:
    stencils_dict = json.load(f)


async def fetch_stencil(data):
    try:
        # Parse the outer JSON string to get the dictionary
        outer_data = json.loads(data)

        # Parse the inner JSON string to get the actual data
        data_list = json.loads(outer_data["data"])

        # Initialize an empty dictionary to hold the transformed data
        transformed_data = {}

        # Iterate over the list of lists, transforming each item
        for i, item in enumerate(data_list, start=1):
            suggestion_name = item[0]
            score = item[1]

            # Check if the suggestion_name is present in stencils_dict
            if suggestion_name in stencils_dict:
                # If present, use the data from stencils_dict
                stencil_data = stencils_dict[suggestion_name]
                suggestion_dict = {"score": score, "stencil": stencil_data}
            else:
                # If not present, indicate it's not in the stencils database
                suggestion_dict = {"suggestion": "Not present in stencils database"}

            # Add the suggestion dictionary to the transformed data dictionary
            transformed_data[suggestion_name] = suggestion_dict

        return transformed_data
    except Exception as e:
        # Handle parsing errors here
        raise ValueError(f"Failed to parse data: {str(e)}")
