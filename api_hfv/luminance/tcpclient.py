import socket
import os


def client(ip, port, message):
    """
    查询函数
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    try:
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        print(response)

    finally:
        s.close()


if __name__ == "__main__":
    HOST, PORT = os.getenv('HOST'), 8085
    msg1 = '1'
    client(HOST, PORT, msg1)
