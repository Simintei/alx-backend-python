
# Django-Middleware-0x03/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Called once when the server starts.
        get_response is the next middleware or view.
        """
        self.get_response = get_response

        # Configure logger to write to a file
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler('requests.log')  # File in project root
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def __call__(self, request):
        """
        Called on every request.
        Logs timestamp, user, and request path.
        """
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        # Continue to the next middleware/view
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to the messaging app between 6PM and 9PM only."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # --- adjust times here ---
        start_hour = 18  # 6 PM
        end_hour = 21    # 9 PM

        # Get current server hour
        current_hour = datetime.now().hour

        # If outside allowed time window
        if current_hour < start_hour or current_hour >= end_hour:
            # Optionally limit to /messaging/ URLs only
            if request.path.startswith('/messaging'):  
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>Access to the messaging app is restricted between 6PM and 9PM.</p>"
                )

        # Otherwise proceed normally
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # {ip: [timestamps]}
        self.message_log = {}

    def __call__(self, request):
        # Only apply to POST requests (sending messages)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize list for IP if not exists
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Keep only timestamps within the last 60 seconds
            self.message_log[ip] = [
                t for t in self.message_log[ip] if now - t < 60
            ]

            # Check the limit
            if len(self.message_log[ip]) >= 5:  # > 5 per minute
                return HttpResponseForbidden(
                    "You have exceeded the message limit. Please wait a minute before sending more."
                )

            # Add current request timestamp
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get client IP address even behind a proxy"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
