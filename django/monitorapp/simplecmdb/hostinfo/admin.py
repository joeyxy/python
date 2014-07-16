from models import Host,HostGroup,Monitor,tq_admin
from django.contrib import admin

class HostAdmin(admin.ModelAdmin):
	list_display = ['vendor','sn','product','cpu_model','cpu_num','cpu_vendor','memory_part_number','memory_manufacturer','memory_size','device_model','device_version','device_sn','device_size','osver','hostname','os_release']

class HostGroupAdmin(admin.ModelAdmin):
	list_display = ['name',]

class MonitorAdmin(admin.ModelAdmin):
    list_display=['ip','time','game','app','pid','useage']


class tq_adminAdmin(admin.ModelAdmin):
    list_display=['ip','time','zone','app','ops','status','runtime']

admin.site.register(HostGroup,HostGroupAdmin)
admin.site.register(Host,HostAdmin)
admin.site.register(Monitor,MonitorAdmin)
admin.site.register(tq_admin,tq_adminAdmin)
