import logging
from datetime import datetime


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