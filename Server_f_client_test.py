import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8888))

sock.listen(1)
conn, addr = sock.accept()

print('Connection is set: ', addr)

response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'

with conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        request = data.decode('utf-8')
        print(f'Recieved request: {ascii(request)}')
        print(f'The answer is send {ascii(response.decode("utf-8"))}')
        conn.send(response)
