import requests

from api.config import DEFAULT_HEADERS, REQUEST_TIMEOUT


class HttpClient:
    def __init__(self, base_url, default_headers=None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        if default_headers:
            self.session.headers.update(default_headers)

    def request(self, method, path, **kwargs):
        url = self.base_url if not path else f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        return self.session.request(method, url, **kwargs)

    def get(self, path="", **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path="", **kwargs):
        return self.request("POST", path, **kwargs)

    def patch(self, path="", **kwargs):
        return self.request("PATCH", path, **kwargs)
