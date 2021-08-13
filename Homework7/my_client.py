import socket
import sys


host = '127.0.0.1'
port = 5050


def client():
    try:
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port+1))
            try:
                print('Input your message')
                message = input().encode()
                print(f'Sending message: {message} from {host} {port+1}')
                print(f'Size of message: {sys.getsizeof(message)}')
                s.connect((host, port))
                s.sendall(message)
                print('Waiting an answer from server')
                data = s.recv(1024)
                print(f'Answer from server: {data}')
                if data != b'ok':
                    raise Exception
            except ConnectionRefusedError as error:
                print(f'Error {error}')

    except Exception as e:
        print('Exception {!r}'.format(e))
        raise Exception


if __name__ == '__main__':
    client()
