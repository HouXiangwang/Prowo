import threading
import socketserver
import subprocess
import logging


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    路由器监听程序
    负责监听设备接入请求，部署应用
    """
    def handle(self):
        logger = logging.getLogger("TCPServer")
        data = self.request.recv(1024).decode()
        (status, output) = subprocess.getstatusoutput('python3 tcpclient.py')
        jresp = output
        self.request.sendall(jresp.encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__": 
    HOST, PORT = "0.0.0.0", 3000
    
    logger = logging.getLogger("TCPServer")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("1.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -\
%(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    logger.info("Program started")
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("Server loop running in thread:" + server_thread.name)
    logger.info(" .... waiting for connection")

    # 使用Ctrl + C退出程序
    server.serve_forever()
