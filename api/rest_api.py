from api.config import DEFAULT_USER_ID, REST_BASE_URL
from api.http_client import HttpClient


class RestApi(HttpClient):
    def __init__(self):
        super().__init__(REST_BASE_URL)

    def create_post(self, title, body, user_id=DEFAULT_USER_ID):
        return self.post("/posts", json={"title": title, "body": body, "user_id": user_id})

    def patch_post(self, post_id, **fields):
        return self.patch(f"/posts/{post_id}", json=fields)

    def get_post(self, post_id):
        return self.get(f"/posts/{post_id}")
