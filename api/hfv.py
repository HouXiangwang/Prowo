import subprocess
import os

import db


def dht11_temp_humi(equip, mode):
    '''
    获取温湿度api接口
    '''
    result = db.find(equip)
    if result is None:
        return (False, 'not found this equip')
    (ipaddr, port) = result
    if mode == 'host' or mode == 'host_remote' or mode == 'docker_remote':
        ipaddr = os.getenv('HFV_HOST')
    elif mode == 'docker':
        ipaddr = equip
        port = 3000
    else:
        return (False, 'no this mode')

    cmd = 'python3 send.py ' + ipaddr + ' ' + str(port) + ' temp'
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        (temp, humi) = output.split('&')
        return (temp, humi)
    else:
        return (False, output)


def switch(equip, mode, method):
    result = db.find(equip)
    if result is None:
        return (False, 'not found this equip')
    (ipaddr, port) = result
    if mode == 'host' or mode == 'host_remote' or mode == 'docker_remote':
        ipaddr = os.getenv('HFV_HOST')
    elif mode == 'docker':
        ipaddr = equip
        port = 3000
    else:
        return (False, 'no this mode')

    cmd = 'python3 send.py ' + ipaddr + ' ' + str(port) + ' ' + method
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        return output
    else:
        return (False, output)


if __name__ == '__main__':
    print(dht11_temp_humi('dht11v2.0','host'))
