from jose import jwt, exceptions
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed

from task_manager import settings
from projects.schemas.dto import User


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (token := request.headers.get("Authorization")):
            raise AuthenticationFailed("No token provided")

        try:
            jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except exceptions.ExpiredSignatureError:
            return JsonResponse({"detail": "Token has expired"}, status=401)
        except exceptions.JWTClaimsError as e:
            return JsonResponse({"detail": f"Invalid claims: {str(e)}"}, status=401)
        except exceptions.JWTError:
            return JsonResponse({"detail": "Invalid token"}, status=403)

        claims = jwt.get_unverified_claims(token)
        if "id" not in claims or "permissions" not in claims.keys():
            raise Exception("Invalid JWT token!")

        user_data = User(id=int(claims["id"]), permissions=claims["permissions"])
        request.user_data = user_data
        return self.get_response(request)
