import os
import socket
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv

from helpers import handle_client


def main():
    load_dotenv(find_dotenv())
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
