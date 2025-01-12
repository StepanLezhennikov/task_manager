from django.utils.deprecation import MiddlewareMixin


class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user_id = 1
        request.user_email = "stepanlezennikov@gmail.com"
