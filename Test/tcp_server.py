import socket


def server():
    host = socket.gethostname()  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    client_socket, adress = s.accept()
    print("Connection from: " + str(adress))
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print('From online user: ' + data)
        data = data.upper()
        client_socket.send(data.encode('utf-8'))
    client_socket.close()


if __name__ == '__main__':
    server()