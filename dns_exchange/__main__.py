import json
import os
import re
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Union

from dotenv import load_dotenv, find_dotenv

from dns_exchange.dictionaries import commands_dict


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


def register_command(func: Callable) -> Callable:
    commands_dict[func.__name__] = func
    return func


def register_all_commands():
    pass


def handle_request(request) -> Union[Response, None]:
    try:
        command_func = commands_dict.get(request.command_name)
        if command_func is None:
            raise ValueError('Unknown command')
        return command_func(**request.command_kwargs)
    except StopIteration:
        return None


def handle_client(conn, addr):
    print(f'Using thread {threading.get_ident()} for client: {addr}!')

    read_file = conn.makefile(mode='r', encoding='utf-8')
    write_file = conn.makefile(mode='w', encoding='utf-8')
    write_file.write('You\'ve successfully connected!\n')
    write_file.flush()

    client_data = read_file.readline().strip()

    while client_data:
        try:
            request_data = re.search("start;(.*)end;", client_data).group(1)
            request = Request.get_from_json_string(request_data)
            response = handle_request(request)
            response_data = response.get_json_string()
        except Exception as e:
            response_data = Response(errors=[str(e)]).get_json_string()

        if response_data is None:
            break

        write_file.write(f'start;{response_data}end;' + '\n')
        write_file.flush()

        client_data = read_file.readline().strip()

    conn.close()


def main():
    load_dotenv(find_dotenv())
    register_all_commands()
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    print(f'Started process with PID={os.getpid()}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)

        with ThreadPoolExecutor(max_workers=2) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(handle_client, conn, addr)


if __name__ == '__main__':
    main()
