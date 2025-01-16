from projects.schemas.dto import User


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_data = User(id=1, email="stepanlezennikov@gmail.com", role="admin")
        request.user_data = user_data
        response = self.get_response(request)
        return response
