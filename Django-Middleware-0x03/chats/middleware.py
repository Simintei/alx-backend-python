
# Django-Middleware-0x03/middleware.py
import logging
from datetime import datetime

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
