import os
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv

# No inspection is added because these imports register command functions
# noinspection PyUnresolvedReferences
from commands import get_value, set_value, bye
from src.dictionaries import commands_dict


def handle_command(cmd, *args):
    try:
        command_func = commands_dict.get(cmd)
        if command_func is None:
            raise ValueError('Unknown command')
        result = command_func(*args)
    except (TypeError, ValueError, AssertionError) as e:
        result = str(e)
    except StopIteration:
        result = ''
    return result


def handle_client(conn, addr):
    print(f'Using thread {threading.get_ident()} for client: {addr}')
    read_file = conn.makefile(mode='r', encoding='utf-8')
    write_file = conn.makefile(mode='w', encoding='utf-8')
    write_file.write('Hi client\n')
    write_file.flush()
    cmd = read_file.readline().strip()
    while cmd:
        result = handle_command(*cmd.split())
        if result == '':
            break
        write_file.write(result + '\n')
        write_file.flush()
        cmd = read_file.readline().strip()
    conn.close()


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
