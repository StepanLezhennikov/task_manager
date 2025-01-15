class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_id = 1
        request.user_email = "stepanlezennikov@gmail.com"
        response = self.get_response(request)
        return response
