from asgiref.sync import sync_to_async
from django.utils import timezone
from main.models import ApiUsageLog
from django.core.exceptions import ObjectDoesNotExist


@sync_to_async
def log_api_usage(google_api_calls=0, unsplash_api_calls=0, pexels_api_calls=0):
    try:
        # Attempt to get the latest log entry
        latest_log = ApiUsageLog.objects.latest("created_at")
        latest_log.google_api_calls = (
            latest_log.google_api_calls + google_api_calls
            if latest_log.google_api_calls is not None
            else google_api_calls
        )
        latest_log.unsplash_api_calls = (
            latest_log.unsplash_api_calls + unsplash_api_calls
            if latest_log.unsplash_api_calls is not None
            else unsplash_api_calls
        )
        latest_log.pexels_api_calls = (
            latest_log.pexels_api_calls + pexels_api_calls
            if latest_log.pexels_api_calls is not None
            else pexels_api_calls
        )
        latest_log.updated_at = timezone.now()
        latest_log.save()
    except ObjectDoesNotExist:
        # Handle the case where no ApiUsageLog object exists
        # For example, create a new ApiUsageLog object
        ApiUsageLog.objects.create(
            google_api_calls=google_api_calls,
            unsplash_api_calls=unsplash_api_calls,
            pexels_api_calls=pexels_api_calls,
        )


@sync_to_async
def extract_items(data):
    item_list = [value["item_name"] for value in data.values()]
    return item_list
