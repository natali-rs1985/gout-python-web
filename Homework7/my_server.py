import socket


host = '127.0.0.1'
port = 5050


def server():
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        print(f'Listening {host} {port}')
        s.listen(1)
        print('Ready to accept data from client')
        conn, addr = s.accept()
        with conn:
            print('Connection from', addr)
            while True:
                data = conn.recv(1024)
                print(f'Received data: {data}')
                if not data == b'':
                    break
            print('Input your answer')
            answer = input().encode()
            conn.sendall(answer)


if __name__ == '__main__':
    server()