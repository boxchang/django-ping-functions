import json

from ping.func import call_subnet_ping

ip = '127.0.0.0/30'
result = call_subnet_ping(ip)
# # sorted(result.items(), key=lambda item:item[1])
# result.sort(key=lambda d:d['short'])
#
#print(result)
# xx="xx"

#l = [{"id": 3, "name": "john"}, {"id": 2, "name": "brandon"}, {"id": 1, "name": "susan"}]
l = json.loads(result)
#l = [{"id": "245", "ip": "127.0.0.245", "result": 1, "style": "background:#a9c9a4;color:#ffffff", "short": ".245"}, {"id": "253", "ip": "127.0.0.253", "result": 1, "style": "background:#a9c9a4;color:#ffffff", "short": ".253"}, {"id": "2", "ip": "127.0.0.2", "result": 1, "style": "background:#a9c9a4;color:#ffffff", "short": ".2"}]
print(l)

# def my_func(d):
#     return d['id']
#
# l.sort(key=my_func)
l.sort(key=lambda d:d['short'])
print(l)