import socket
import os


def client(ip, port, message):
    """
    设备接入函数
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    try:
        print("Send:"+message)
        s.sendall(message.encode())
        response = s.recv(1024).decode()
        print(str(response))

    finally:
        s.close()


if __name__ == "__main__":
    HOST, PORT = os.getenv('HOST'), 8085

    msg1 = 'on'
    client(HOST, PORT, msg1)
