class Response:
    def __init__(self, auth_token: str = '', content=None, errors=None):
        self.auth_token = auth_token
        self.content = content if content else []
        self.errors = errors if errors else []
