class BaseError(Exception):
    pass


class RequestError(BaseError):

    def __init__(self, url, exc):
        self.url = url
        self.exc = exc

    def __str__(self):
        return f"RequestError: {self.exc}, url:{self.url}"
