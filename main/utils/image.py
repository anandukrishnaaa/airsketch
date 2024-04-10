import aiohttp
import asyncio
import json
from dotenv import load_dotenv
import os
from ._helper import log_api_usage

load_dotenv()

UNSPLASH_API_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_API_URL = "https://api.pexels.com/v1/search"

PER_PAGE = 5
PAGE = 1


async def fetch_images_by_keyword_unsplsh(keyword, uuid, chained=False, single=False):
    async with aiohttp.ClientSession() as session:
        results = {}

        async def fetch_single_image(query):
            params = {
                "query": query,
                "client_id": UNSPLASH_API_KEY,
                "per_page": PER_PAGE,
                "page": PAGE,
            }
            try:
                async with session.get(UNSPLASH_API_URL, params=params) as response:
                    await log_api_usage(unsplash_api_calls=1, uuid=uuid)
                    if response.status == 200:
                        data = await response.json()
                        images = []
                        for image_data in data["results"]:
                            image_info = {
                                "regular": image_data["urls"]["regular"],
                                "description": image_data["description"],
                                "alt_description": image_data["alt_description"],
                                "username": image_data["user"]["username"],
                                "download": image_data["links"]["download"],
                            }
                            images.append(image_info)
                        return images
                    else:
                        return [
                            {
                                "error": "Failed to fetch images. Status code: "
                                + str(response.status)
                            }
                        ]
            except Exception as e:
                return [{"error": str(e)}]

        if single:
            if isinstance(keyword, str):
                keyword = [keyword]
            for kw in keyword:
                results[kw] = await fetch_single_image(kw)
        else:
            unique_keywords = list(set(keyword))
            query = "+".join(unique_keywords) if chained else " ".join(unique_keywords)
            results[query] = await fetch_single_image(query)
        return results


async def fetch_images_by_keyword_pxls(keyword, uuid, chained=False, single=False):
    async with aiohttp.ClientSession() as session:
        results = {}

        async def fetch_single_image(query):
            headers = {"Authorization": PEXELS_API_KEY}
            params = {
                "query": query,
                "per_page": PER_PAGE,
                "page": PAGE,
            }
            try:
                async with session.get(
                    PEXELS_API_URL, headers=headers, params=params
                ) as response:
                    await log_api_usage(pexels_api_calls=1, uuid=uuid)
                    if response.status == 200:
                        data = await response.json()
                        images = []
                        for photo in data["photos"]:
                            image_info = {
                                "regular": photo["src"]["large"],
                                "description": photo["alt"],
                                "alt_description": photo["alt"],
                                "username": photo["photographer"],
                                "download": photo["url"],
                            }
                            images.append(image_info)
                        return images
                    else:
                        return [
                            {
                                "error": "Failed to fetch images. Status code: "
                                + str(response.status)
                            }
                        ]
            except Exception as e:
                return [{"error": str(e)}]

        if single:
            if isinstance(keyword, str):
                keyword = [keyword]
            for kw in keyword:
                results[kw] = await fetch_single_image(kw)
        else:
            unique_keywords = list(set(keyword))
            query = "+".join(unique_keywords) if chained else " ".join(unique_keywords)
            results[query] = await fetch_single_image(query)
        return results
