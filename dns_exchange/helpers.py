import json
from typing import List


class Request:
    def __init__(self, command, auth_token: str = "", args=None):
        self.auth_token = auth_token
        self.command_name = command
        self.command_kwargs = args if args else {}

    @classmethod
    def get_from_json_string(cls, json_string):
        return cls(**json.loads(json_string))


class Response:
    def __init__(self, auth_token: str = "", content=None, errors=None):
        self.auth_token = auth_token
        self.content = content if content else []
        self.errors = errors if errors else []

    def get_json_string(self) -> str:
        return json.dumps(
            {
                "auth_token": self.auth_token,
                "content": self.content,
                "errors": self.errors,
            }
        )

    def add_content_text(self, title: str = "", lines: List[str] = None) -> None:
        self.content.append({"type": "text", "title": title, "lines": lines if lines else []})

    def add_content_table(self, name: str = "", headers: List[str] = None, rows: List[List[str]] = None) -> None:
        self.content.append(
            {
                "type": "table",
                "name": name,
                "headers": headers if headers else [],
                "rows": rows if rows else [],
            }
        )

    def add_error(self, error_text: str) -> None:
        self.errors.append(error_text)
