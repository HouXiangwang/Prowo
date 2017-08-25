import socket
import sys
import json


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
    HOST, PORT = sys.argv[1],int(sys.argv[2])
    msg1 = {'cmd': r'', 'equip': "dht11", 'log': "up", 'repo': "joliu", 'imname': "hfv/dht11:v2.0", "dcport": "33333", "ip": "127.0.0.1"}
    jmsg1 = json.dumps(msg1)
    client(HOST, PORT, jmsg1)
