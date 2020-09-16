# Test connection.
import socket

sock = socket.socket()
sock.bind(('', 8888))

sock.listen(1)
conn, addr = sock.accept()

print('Connection is set: ', addr)

response = b''      # change 'response' to test the client

with conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        request = data.decode('utf-8')
        print(f'Recieved request: {ascii(request)}')
        print(f'The answer is send {ascii(response.decode("utf-8"))}')
        conn.send(response)
