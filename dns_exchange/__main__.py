import os
import re
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Union

from bson import ObjectId

from dns_exchange import config
from dns_exchange.dictionaries import commands_dict
from dns_exchange.helpers import Request, Response
from dns_exchange.models.mongo.users import User
from dns_exchange.registers import register_all_commands


def handle_request(request) -> Union[Response, None]:
    command_func = commands_dict.get(request.command_name)
    if command_func is None:
        raise ValueError("Unknown command")
    return command_func(**request.command_kwargs)


def handle_client(conn, addr):
    print(f"Using thread {threading.get_ident()} for client: {addr}!")

    read_file = conn.makefile(mode="r", encoding="utf-8")
    write_file = conn.makefile(mode="w", encoding="utf-8")

    response = Response()
    response.add_content_text(title="You've successfully connected!")
    response_data = response.get_json_string()
    write_file.write(f"start;{response_data}end;\n")
    write_file.flush()

    client_data = read_file.readline().strip()

    while client_data:
        request_data = re.search("start;(.*)end;", client_data).group(1)
        request = Request.get_from_json_string(request_data)

        try:
            response = handle_request(request)
        except Exception as e:
            response = Response()
            response.add_error(str(e))

        if response.auth_token == '':
            response.auth_token = request.auth_token
        response_data = response.get_json_string()

        write_file.write(f"start;{response_data}end;\n")
        write_file.flush()

        client_data = read_file.readline().strip()

    conn.close()


def main():
    register_all_commands()
    print(f"Started process with PID={os.getpid()}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((config.HOST, config.PORT))
        s.listen(5)

        with ThreadPoolExecutor(max_workers=2) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(handle_client, conn, addr)


if __name__ == "__main__":
    # main()

    user = User.retrieve(id='61b4e669135ff8f08163d3cc')
    for key, val in user.assets:
        print(key, val)
