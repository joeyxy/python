from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Host,HostGroup

try:
	import json
except ImportError,e:
	import simlejson as json

def collect(request):
	req = request
	if req.POST:
		memory_size = req.POST.get('Size')
		ipaddrs = req.POST.get('Ipaddr')
		hostname = req.POST.get('os_name')
		host = Host()
		host.hostname=hostname
		host.memory_size=memory_size
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
		d.append(ret_hg)
	ret = {'status':0,'data':d,'mesage':'ok'}
	return HttpResponse(json.dumps(ret))
