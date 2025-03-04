from typing import Dict
from unittest.mock import MagicMock, patch

import pytest
from jose import jwt
from rest_framework.test import APIClient


def create_jwt_token(
    user_id: int | None = None, permissions: list[str] | None = None
) -> str:
    payload = {}
    if user_id is not None:
        payload.update({"id": str(user_id)})
    if permissions is not None:
        payload.update({"permissions": permissions})
    return jwt.encode(payload, "super_secret_key", algorithm="HS256")


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    client = APIClient()
    return client


@pytest.fixture
def admin_headers() -> Dict[str, str]:
    return {"Authorization": create_jwt_token(user_id=1, permissions=[])}


@pytest.fixture
def mock_httpx_get():
    with patch("httpx.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = [{"email": "test@example.com"}]
        mock_get.return_value = mock_response
        yield mock_get
