import socket
import sys


def client(ip, port, message):
    """
    设备接入函数
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
    HOST, PORT, msg= sys.argv[1], int(sys.argv[2]), sys.argv[3]
    client(HOST, PORT, msg)
