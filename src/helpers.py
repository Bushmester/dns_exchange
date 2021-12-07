import threading

from src.dictionaries import commands_dict


def register_command(func):
    commands_dict[func.__name__] = func
    return func


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
