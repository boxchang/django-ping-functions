import json
import os
from threading import Thread
import subprocess
import queue
from IPy import IP #调用IP



# some global vars
num_threads = 15
ips_q = queue.Queue()
out_q = queue.Queue()
results = []

def call_ping(ip):
    ips_q.put(ip)
    worker = Thread(target=thread_pinger, args=(0, ips_q))
    worker.setDaemon(True)
    worker.start()
    ips_q.join()
    return json.dumps(results)


def call_subnet_ping(ip_d):
    ips = []
    print('ip_d:'+str(ip_d))
    ip = IP(ip_d)  # 输入192.168.1.0/24网段
    print(ip.len())  # 192.168.1.0/24的网段的IP个数
    for x in ip:
        print(x)  # 输出192.168.1.0/24网段所有的ip清单
        ips.append(str(x))


    global results
    results = []
    # start the thread pool
    for i in range(num_threads):
        worker = Thread(target=thread_pinger, args=(i, ips_q))
        worker.setDaemon(True)
        worker.start()

    # fill queue
    for ip in ips:
        ips_q.put(ip)

    # wait until worker threads are done to exit
    ips_q.join()

    # print result
    while True:
        try:
            msg = out_q.get_nowait()
        except queue.Empty:
            break
        print(msg)
    results.sort(key=lambda d: d['id'])
    return json.dumps(results)


def thread_pinger(i, q):
    global results
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
            try:
                result['id'] = int(ip[ip.rfind('.')+1:])
            except ValueError as err:
                print(err)
                print(ip)
                pass
            result['ip'] = ip
            result['result'] = 1
            result['style'] = 'background:#a9c9a4;color:#ffffff'
            result['short'] = ip[ip.rfind('.'):]
            results.append(result)
            out_q.put(str(ip) + " True")
        elif ret==1:
            print('%s is down...'%ip)
            try:
                result['id'] = int(ip[ip.rfind('.')+1:])
            except ValueError as err:
                print(err)
                print(ip)
                pass
            result['ip'] = ip
            result['result'] = 0
            result['style'] = 'background:#ffffff;color:#333333'
            result['short'] = ip[ip.rfind('.'):]
            results.append(result)
            out_q.put(str(ip) + " False")
        q.task_done()


# print(ping('222.0.0.2'))
# print(ping('127.0.0.2'))
# print(subnet_ping('10.231.0.0/24'))