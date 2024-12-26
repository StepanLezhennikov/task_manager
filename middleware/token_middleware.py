from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        # if auth_header.startswith('Bearer '):
        #     token = auth_header[7:]  # Убираем "Bearer "
        #     try:
        #         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        #         request.user_data = payload
        #     except jwt.ExpiredSignatureError:
        #         request.user_data = None
        #     except jwt.InvalidTokenError:
        #         request.user_data = None
        # else:
        #     request.user_data = None
        request.user_id = 1
        request.user_email = 'stepanlezennikov@gmail.com'
