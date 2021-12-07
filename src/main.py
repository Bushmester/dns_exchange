import os
import socket
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv

from src.helpers import handle_client

# No inspection is added because these imports register command functions
# noinspection PyUnresolvedReferences
from src.commands.test import echo


def main():
    load_dotenv(find_dotenv())
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    print(f'Started process with PID={os.getpid()}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # solution for "[Error 89] Address already in use". Use before bind()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)

        #  Proper threads termination doesn't work here, use SIGKILL
        with ThreadPoolExecutor(max_workers=2) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(handle_client, conn, addr)


if __name__ == '__main__':
    main()
