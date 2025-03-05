import httpx


class AuthAPI:
    base_url = "http://user_management:8001/v1"

    @classmethod
    def get_email_by_id(cls, user_id: int) -> str:
        response = httpx.get(
            cls.base_url
            + "/users/?limit=10&offset=0&sort_by=created_at&sort_order=asc&id={}".format(
                str(user_id)
            )
        )
        email = response.json()[0]["email"]
        return email
