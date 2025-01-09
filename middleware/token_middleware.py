from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user_id = 1
        request.user_email = "stepanlezennikov@gmail.com"
