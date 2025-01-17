from jose import jwt
from rest_framework.exceptions import AuthenticationFailed

from projects.schemas.dto import User


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (token := request.headers.get("Authorization")):
            raise AuthenticationFailed("No token provided")

        claims = jwt.get_unverified_claims(token)
        if "id" not in claims or "role" not in claims.keys():
            raise Exception("Invalid JWT token!")

        user_data = User(id=int(claims["id"]), role=claims["role"])
        request.user_data = user_data
        return self.get_response(request)
