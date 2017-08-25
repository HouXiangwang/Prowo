import threading
import socketserver
import json
import time
import logging
import subprocess

import buildDock
import db


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    路由器监听程序
    负责监听设备接入请求，部署应用
    """
    def handle(self):
        logger = logging.getLogger("TCPServer")
        data = self.request.recv(1024).decode()
        jdata = json.loads(data)
        logger.info("Receive data from '%r'"% (data))
        rec_equip = jdata['equip']
        rec_log = jdata['log']
        repo = jdata['repo']
        imname = jdata['imname']
        rec_cmd = jdata['cmd']
        rec_ipaddr = jdata['ip']
        if rec_log == 'up':
            status = 0
            timel = str(time.time()).split('.')[0]
            print("new equip:"+rec_equip)
            sql = "insert into equipdb (equip,status,signintime,dockername,\
            ipaddress) values ('" + rec_equip + "'," + str(status) + "," + str(timel) + ",'" + imname + "','"+rec_ipaddr+"')"
            db.exec(sql)
            log_ans = True
            if not buildDock.checkim(imname):
                if buildDock.pulldc(imname):
                    flag = buildDock.run(imname, rec_equip, rec_cmd, rec_ipaddr)
                    if flag[0]:
                        cmd_ans = True
                    else:
                        cmd_ans = False
                else:
                    print('pull failed')
                    cmd_ans = False
            else:
                if buildDock.checkdc(rec_equip):
                    flag = buildDock.start(rec_equip)
                    if flag[0]:
                        cmd_ans = True
                    else:
                        cmd_ans = False

                else:
                    flag = buildDock.run(imname, rec_equip, rec_cmd, rec_ipaddr)
                    if flag[0]:
                        cmd_ans = True
                    else:
                        cmd_ans = False
   
        elif rec_log == 'in':
            status = 1
            timel = 1
            sql = 'update equipdb set status=1 where equip="'+rec_equip+"'"
            db.exec(sql)
            log_ans = True
            if builDock.start(rec_equip) and log_ans:
                cmd_ans = True
            else:
                cmd_ans = False
        else:
            log_ans = False
            cmd_ans = False
 
        cur_thread = threading.current_thread()
        response = {'equip': rec_equip, 'log_ans': log_ans, 'cmd_ans': cmd_ans, 'port': flag[1]}
        jresp = json.dumps(response)
        self.request.sendall(jresp.encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    cmd = 'docker start test-mysql'
    (status, output) = subprocess.getstatusoutput(cmd)
    if status != 0:
        exit(0)
    print('started!')
    HOST, PORT = "0.0.0.0", 22223
    
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
