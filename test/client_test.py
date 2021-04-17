import requests
import time
import psutil
import json

HOSTNAME = 'Client1'
HOSTIP = '42.234.107.236'
SERVER_IP = '193.112.109.51'
SERVER_PORT = '5000'
SERVER_POST_PATH = '/update_data/'
STEPS = '60'

def StrOfSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, round(remainder / 1024, 2), level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level+1 > len(units):
        level = -1
    return ( '{} {}'.format(integer+remainder, units[level]) )


class Client():
    def __init__(self):
        self.s=requests.Session()
        self.headers = {'Content-Type': 'application/json'} 
        self.data={
            'hostname':HOSTNAME,
            HOSTNAME:{
                'host_ip': HOSTIP,
                'cpu_count':'',
                'cpu_percent':'',
                'memory_size':'',
                'memory_percent':'',
                'swap_size':'',
                'swap_percent':'',
            }
        }
    def get_status(self):
        self.data[HOSTNAME]['cpu_count']=psutil.cpu_count(logical=True)
        self.data[HOSTNAME]['cpu_percent']=psutil.cpu_percent()
        self.data[HOSTNAME]['memory_size']=StrOfSize(psutil.virtual_memory().total)
        self.data[HOSTNAME]['memory_percent']=psutil.virtual_memory().percent
        self.data[HOSTNAME]['swap_size']=StrOfSize(psutil.swap_memory().total)
        self.data[HOSTNAME]['swap_percent']=psutil.swap_memory().percent
        print(json.dumps(self.data,indent=4))
        
    def update_status(self):
        res=self.s.post(url='http://'+SERVER_IP+':'+SERVER_PORT+SERVER_POST_PATH,headers= self.headers,data=json.dumps(self.data))
        print(res.text)


if __name__ == '__main__':
    c=Client()
    for _ in range(1):
        c.get_status()
        c.update_status()
        time.sleep(int(STEPS))
    