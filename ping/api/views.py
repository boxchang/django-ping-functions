import json

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ping.func import SubnetPing


@csrf_exempt
def subnet_ping(request):
    if request.method == 'POST':
        ip = request.POST.get('ip')
        # result = json.dumps({'127.0.0.1': True})
        print('web_ip:'+str(ip))
        subnetping = SubnetPing()
        result = subnetping.call_subnet_ping(ip)
        return HttpResponse(result, content_type="application/json")
    else:
        raise Http404

@csrf_exempt
def ping(request):
    if request.method == 'POST':
        ip = request.POST.get('ip')
        subnetping = SubnetPing()
        result = subnetping.call_ping(ip)
        return HttpResponse(result, content_type="application/json")
    else:
        raise Http404




