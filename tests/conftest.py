from typing import Dict

import pytest
from jose import jwt
from rest_framework.test import APIClient

from projects.schemas.dto import Role


def create_jwt_token(user_id: int | None = None, role: Role | None = None) -> str:
    payload = {}
    if user_id is not None:
        payload.update({"id": str(user_id)})
    if role is not None:
        payload.update({"role": str(role)})
    return jwt.encode(payload, "super_secret_key", algorithm="HS256")


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    client = APIClient()
    return client


@pytest.fixture
def admin_headers() -> Dict[str, str]:
    return {"Authorization": create_jwt_token(user_id=1, role=Role.ADMIN)}
