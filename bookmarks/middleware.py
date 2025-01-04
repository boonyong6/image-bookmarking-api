import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class LogRequestMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        logger.warning(f"Request headers: {dict(request.headers)}")
        logger.warning(f"Request body: {request.body.decode()}")

        response = self.get_response(request)
        return response
