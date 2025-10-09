import logging
from datetime import datetime, timezone
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone as dj_timezone
from django.core.cache import cache


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


class OffensiveLanguageMiddleware:
    """
        Middleware that limits the number of chat messages a user can send within a certain time window, based on thier IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.window_seconds = int(getattr(settings, 'CHAT_RATE_LIMIT_WINDOW_SECONDS', 60))
        self.max_messages = int(getattr(settings, 'CHAT_RATE_LIMIT_MAX_MESSAGES', 5))
        # Path to applly the Rate Limit to
        self.path_prefixes = tuple(getattr(
            settings,
            'CHAT_MESSAGE_PATH_PREFIXES',
            ('/api/messages', '/messages')
        ))

    def _client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

    def __call__(self, request):
        if request.method.upper() == "POST" and any(request.path.startswith(p) for p in self.path_prefixes):
            ip = self._client_ip(request)
            cache_key = f"chat_rate:{ip}"
            now_ts = dj_timezone.now().timestamp()

            timestamps = cache.get(cache_key, [])
            cutoff = now_ts - self.window_seconds
            timestamps = [ts for ts in timestamps if ts > cutoff]

            if len(timestamps) >= self.max_messages:
                retry_after = int(timestamps[0] + self.window_seconds - now_ts) if timestamps else self.window_seconds
                detail = f"Rate limit exceeded: max {self.max_messages} messages per {self.window_seconds} seconds."
                 return JsonResponse({'detail': detail}, status=429, headers={'Retry-After': str(max(retry_after, 1))})

            timestamps.append(now_ts)
            cache.set(cache_key, timestamps, timeout=self.window_seconds)

    return self.get_response(request)


class RolepermissionMiddleware:
    """
        Middleware that restricts access to certain views based on user roles.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_roles = set(getattr(settings, 'ROLE_PERMISSION_ALLOWED_ROLES', ('admin', 'moderator')))
        self.exempt_prefixes = tuple(getattr(
            settings,
            'ROLE_PERMISSION_EXEMPT_PATH_PREFIXES',
            ('/admin', '/api/token', '/api/token/refresh', '/static', '/media')
        ))

    def __call__(self, request):
        # Skip checks for exempt paths
        if any(request.path.startswith(p) for p in self.exempt_prefixes):
            return self.get_response(request)

        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return JsonResponse({'detail': 'Forbidden: authentication required.'}, status=403)

        # Superusers always allowed
        if getattr(user, 'is_superuser', False):
            return self.get_response(request)

        role = getattr(user, 'role', None)
        if role not in self.allowed_roles:
            return JsonResponse({'detail': 'Access forbidden: insufficient role permissions.'}, status=403)

        return self.get_response(request)