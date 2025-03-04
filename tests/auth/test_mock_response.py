from api.auth import AuthAPI


def test_get_email_by_id(mock_httpx_get):
    user_id = 1
    email = AuthAPI.get_email_by_id(user_id)

    assert email == "test@example.com"
    mock_httpx_get.assert_called_once_with(
        "http://user_management:8001/v1/users/?limit=10&offset=0&sort_by=created_at&sort_order=asc&id=1"
    )
