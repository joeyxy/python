from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Host,HostGroup,Monitor,tq_admin

try:
	import json
except ImportError,e:
	import simlejson as json

def collect(request):
    req = request
    if req.POST:
        vendor = req.POST.get('Product_Name')
        sn = req.POST.get('Serial_Number')
        product = req.POST.get('Manufacturer')
        cpu_model = req.POST.get('Model_Name')
        cpu_num = req.POST.get('Cpu_Cores')
        cpu_vendor = req.POST.get('Vendor_Id')
        memory_part_number = req.POST.get('Part_Number')
        memory_manufacturer = req.POST.get('Manufacturer')
        memory_size = req.POST.get('Size')
        device_model = req.POST.get('Device_Model')
        device_version = req.POST.get('Firmware_Version')
        device_sn = req.POST.get('Serial_Number')
        device_size = req.POST.get('User_Capacity')
        osver = req.POST.get('os_version')
        ipaddrs = req.POST.get('Ipaddr')
        hostname = req.POST.get('os_name')
        os_release = req.POST.get('os_release')
        mac = req.POST.get('Device')
        link = req.POST.get('Link')
        mask = req.POST.get('Mask')
        device = req.POST.get('Device')
        host = Host()
        host.hostname=hostname
        host.product = product
        host.cpu_num = cpu_num
        host.cpu_model = cpu_model
        host.cpu_vendor = cpu_vendor
        host.memory_part_number = memory_part_number
        host.memory_size=memory_size
        host.device_model= device_version
        host.device_version = device_version
        host.device_sn = device_sn
        host.device_size = device_size
        host.osver = osver
        host.os_release = os_release
        host.vendor = vendor
        host.sn = sn
        host.ipaddr = ipaddrs
        host.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('no post data')
		

def gethosts(req):
    d = []
    hostgroups = HostGroup.objects.all()
    for hg in hostgroups:
        ret_hg = {'hostgroup':hg.name,'members':[]}
        members = hg.members.all()
        for h in members:
            ret_h = {'hostname':h.hostname,'ipaddr':h.ipaddr}
            ret_hg['members'].append(ret_h)
        d.append(ret_hg)
    ret = {'status':0,'data':d,'mesage':'ok'}
    return HttpResponse(json.dumps(ret))


def monitor_list(request):
    monitors = Monitor.objects.all()
    return render_to_response('monitor_list.html',{'monitors':monitors})

def tq_list(requst):
    tqstatus = tq_admin.objects.all()
    return render_to_response('tq_list.html',{'tqstatus':tqstatus})


def tq_collect(request):
    req = request
    if req.POST:
        ip  = req.POST.get('ip')
        time = req.POST.get('time')
        zone = req.POST.get('zone')
        app = req.POST.get('app')
        ops = req.POST.get('ops')
        status = req.POST.get('status')
        runtime = req.POST.get('runtime')
        tq_list = tq_admin()
        tq_list.ip = ip
        tq_list.time = time
        tq_list.zone=zone
        tq_list.app = app
        tq_list.ops = ops
        tq_list.status = status
        tq_list.runtime = runtime
        tq_list.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('no post data')
def monitor_collect(request):
    req = request
    if req.POST:
        ip = req.POST.get('ip')
        time = req.POST.get('time')
        game = req.POST.get('game')
        app = req.POST.get('app')
        pid = req.POST.get('pid')
        useage = req.POST.get('useage')
        monitor = Monitor()
        monitor.ip = ip
        monitor.time = time
        monitor.game = game
        monitor.app = app
        monitor.pid = pid
        monitor.useage = useage
        monitor.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('no post data')
