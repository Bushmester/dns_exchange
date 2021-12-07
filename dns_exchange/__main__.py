import json
import os
import re
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Union, List

from dns_exchange import config
from dns_exchange.dictionaries import commands_dict
from dns_exchange.helpers import register_all_commands


class Request:
    def __init__(self, command, auth_token: str = '', args=None):
        self.auth_token = auth_token
        self.command_name = command
        self.command_kwargs = args if args else {}

    @classmethod
    def get_from_json_string(cls, json_string):
        return cls(**json.loads(json_string))


class Response:
    def __init__(self, auth_token: str = '', content=None, errors=None):
        self.auth_token = auth_token
        self.content = content if content else []
        self.errors = errors if errors else []

    def get_json_string(self) -> str:
        return json.dumps({"auth_token": self.auth_token, "content": self.content, "errors": self.errors})

    def add_content_text(self, title: str = '', lines: List[str] = None) -> None:
        self.content.append({
            'type': 'text',
            'title': title,
            'lines': lines if lines else []
        })

    def add_content_table(self, name: str = '', headers: List[str] = None, rows: List[List[str]] = None) -> None:
        self.content.append({
            'type': 'table',
            'name': name,
            'headers': headers if headers else [],
            'rows': rows if rows else []
        })

    def add_error(self, error_text: str) -> None:
        self.errors.append(error_text)


def handle_request(request) -> Union[Response, None]:
    command_func = commands_dict.get(request.command_name)
    if command_func is None:
        raise ValueError('Unknown command')
    return command_func(**request.command_kwargs)


def handle_client(conn, addr):
    print(f'Using thread {threading.get_ident()} for client: {addr}!')

    read_file = conn.makefile(mode='r', encoding='utf-8')
    write_file = conn.makefile(mode='w', encoding='utf-8')

    response = Response()
    response.add_content_text(title='You\'ve successfully connected!')
    response_data = response.get_json_string()

    write_file.write(f'start;{response_data}end;')
    write_file.flush()

    client_data = read_file.readline().strip()

    while client_data:
        try:
            request_data = re.search("start;(.*)end;", client_data).group(1)
            request = Request.get_from_json_string(request_data)
            response = handle_request(request)
            response_data = response.get_json_string()
        except Exception as e:
            response = Response()
            response.add_error(str(e))
            response_data = response.get_json_string()

        write_file.write(f'start;{response_data}end;' + '\n')
        write_file.flush()

        client_data = read_file.readline().strip()

    conn.close()


def main():
    register_all_commands()
    print(f'Started process with PID={os.getpid()}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((config.HOST, config.PORT))
        s.listen(5)

        with ThreadPoolExecutor(max_workers=2) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(handle_client, conn, addr)


if __name__ == '__main__':
    main()
