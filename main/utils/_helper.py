from asgiref.sync import sync_to_async
from django.utils import timezone
from main.models import ApiUsageLog, Session
from django.core.exceptions import ObjectDoesNotExist


@sync_to_async
def log_api_usage(uuid, google_api_calls=0, unsplash_api_calls=0, pexels_api_calls=0):
    try:
        # Retrieve the session using the provided UUID
        session = Session.objects.get(session=uuid)

        try:
            # Attempt to get the latest log entry associated with the session
            latest_log = ApiUsageLog.objects.filter(session=session).latest(
                "created_at"
            )
            latest_log.google_api_calls += google_api_calls
            latest_log.unsplash_api_calls += unsplash_api_calls
            latest_log.pexels_api_calls += pexels_api_calls
            latest_log.updated_at = timezone.now()
            latest_log.save()
        except ObjectDoesNotExist:
            # If no log entry exists, create a new one associated with the session
            ApiUsageLog.objects.create(
                session=session,
                google_api_calls=google_api_calls,
                unsplash_api_calls=unsplash_api_calls,
                pexels_api_calls=pexels_api_calls,
            )
    except Session.DoesNotExist:
        # Handle the case where the session with the provided UUID does not exist
        # For example, log an error or perform appropriate error handling
        pass


@sync_to_async
def extract_items(data):
    item_list = [value["item_name"] for value in data.values()]
    return item_list
