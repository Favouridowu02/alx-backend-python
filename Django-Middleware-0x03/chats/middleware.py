import logging
from datetime import datetime, timezone


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file, including the timestamp, user and the requested path.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
        Middleware that restricts access to certain views based on the time of day.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_hour = int(getattr(settings, 'CHAT_ACCESS_START_HOUR', 18))  # Default to 6 PM
        end_hour = int(getattr(settings, 'CHAT_ACCESS_END_HOUR', 21))

        now_local = timezone.localtime(timezone.now())
        hour = now_local.hour


        if start_hour == end_hour:
            allowed = True  # Access allowed all day
        elif start_hour < end_hour:
            allowed = (start_hour <= hour) and (hour < end_hour)
        else:
            allowed = (hour >= start_hour) or (hour < end_hour)

        if not allowed:
            msg = f"Access to chat is restricted to between {start_hour}:00 and {end_hour}:00."
            return JsonResponse({'detail': msg}, status=403)

        return self.get_response(request)