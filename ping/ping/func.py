import json
import os
from threading import Thread
import subprocess
import queue
from IPy import IP #调用IP


class SubnetPing:
    # some global vars
    num_threads = 15
    ips_q = queue.Queue()
    out_q = queue.Queue()

    results = []

    def __init__(self):
        self.results = []


    def call_ping(self, ip):
        self.ips_q.put(ip)
        worker = Thread(target=self.thread_pinger, args=(0, self.ips_q))
        worker.setDaemon(True)
        worker.start()
        self.ips_q.join()
        return json.dumps(self.results)


    def call_subnet_ping(self, ip_d):
        ips = []
        print('ip_d:'+str(ip_d))
        ip = IP(ip_d)  # 输入192.168.1.0/24网段
        print(ip.len())  # 192.168.1.0/24的网段的IP个数
        for x in ip:
            print(x)  # 输出192.168.1.0/24网段所有的ip清单
            ips.append(str(x))

        # start the thread pool
        for i in range(self.num_threads):
            worker = Thread(target=self.thread_pinger, args=(i, self.ips_q))
            worker.setDaemon(True)
            worker.start()

        # fill queue
        for ip in ips:
            self.ips_q.put(ip)

        # wait until worker threads are done to exit
        self.ips_q.join()

        # print result
        while True:
            try:
                msg = self.out_q.get_nowait()
            except queue.Empty:
                break
            print(msg)
        self.results.sort(key=lambda d: d['id'])
        return json.dumps(self.results)


    def thread_pinger(self, i, q):
        while True:
            ip=q.get()
            print('Thread %s pinging %s' %(i,ip) )
            print('OS:' + os.name)
            if os.name=='nt':
                ret = subprocess.call('ping -n 1 %s' % ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                ret = subprocess.call('ping -c 1 -W 1 %s' % ip,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)

            result = {}
            if ret==0:
                print('%s is alive!' %ip)
                result['id'] = int(ip[ip.rfind('.')+1:])
                result['ip'] = ip
                result['result'] = 1
                result['style'] = 'background:#a9c9a4;color:#ffffff'
                result['short'] = ip[ip.rfind('.'):]
                self.results.append(result)
                self.out_q.put(str(ip) + " True")
            elif ret==1:
                print('%s is down...'%ip)
                result['id'] = ip[ip.rfind('.') + 1:]
                result['ip'] = ip
                result['result'] = 0
                result['style'] = 'background:#ffffff;color:#333333'
                result['short'] = ip[ip.rfind('.'):]
                self.results.append(result)
                self.out_q.put(str(ip) + " False")
            q.task_done()


# print(ping('222.0.0.2'))
# print(ping('127.0.0.2'))
# print(subnet_ping('10.231.0.0/24'))