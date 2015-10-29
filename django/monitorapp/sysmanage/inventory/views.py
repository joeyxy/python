# Create your views here.

from django.shortcuts import render_to_response
from health_check import scan_port,scan
import models
import os

#base_dir = '/data/python/django/monitorapp/sysmanage/inventory'

base_dir = '/Users/joey/Documents/code/python/django/monitorapp/sysmanage/inventory'

            
def check(request):
    error = False
    if 'ip' in request.GET and 'port' in request.GET:
        q = request.GET['ip']
        p = request.GET['port']
        if not q :
            error = True
            return render_to_response('check_form.html',{'error':error})
        else:
            result = scan_port(q,p)
            re_ip = request.META['REMOTE_ADDR']
            return render_to_response('check_results.html',{'result':result,'ip':q,'port':p,'re_ip':re_ip})

    else:
        return render_to_response('check_form.html',{'error':error})

def check_list(request):
    error = False
    if 'file' in request.GET:
            f = request.GET['file']
            if not f:
                error =True
                return render_to_response('list_form.html',{'error':error})
            else:
                list = open(os.path.join(base_dir,f),'r')
                result = [scan(l) for l in list]
                list.close()
                return render_to_response('list_results.html',{'result':result,'file':f})
    else:
        return render_to_response('list_form.html',{'error':error})

def main(request):
    os_list = models.OperatingSystem.objects.all()
    svc_list = models.Service.objects.all()
    hardware_list = models.HardwareComponent.objects.all()
    location_list = models.Location.objects.all()
    servers_list = models.Server.objects.all()
    return render_to_response('main.html', {'location_list':location_list,'servers_list':servers_list,'os_list': os_list, 
            'svc_list': svc_list, 'hardware_list': hardware_list})

def categorized(request, category, category_id):
    category_dict = {'loc':'Location','os': 'Operating System', 
        'svc': 'Service', 'hw': 'Hardware'}
    if category == 'loc':
        server_list = models.Server.objects.filter(location__exact=category_id)
        category_name = models.Location.objects.get(id=category_id)
    elif category == 'os':
        server_list = models.Server.objects.filter(os__exact=category_id)
        category_name = models.OperatingSystem.objects.get(id=category_id)
    elif category == 'svc':
        server_list = \
            models.Server.objects.filter(services__exact=category_id)
        category_name = models.Service.objects.get(id=category_id)
    elif category == 'hw':
        server_list = \
            models.Server.objects.filter(hardware_component__exact=category_id)
        category_name = models.HardwareComponent.objects.get(id=category_id)
    else:
        server_list = []
    return render_to_response('categorized.html', {'server_list': server_list, 
        'category': category_dict[category], 'category_name': category_name})

def server_detail(request, server_id):
    server = models.Server.objects.get(id=server_id)
    return render_to_response('server_detail.html', {'server': server})

def server_list(request):
    servers = models.Server.objects.all()
    return render_to_response('server_list.html',{'servers':servers})
