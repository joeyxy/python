from models import Host,HostGroup
from django.contrib import admin

class HostAdmin(admin.ModelAdmin):
	list_display = ['memory_size','hostname']

class HostGroupAdmin(admin.ModelAdmin):
	list_display = ['name',]

admin.site.register(HostGroup,HostGroupAdmin)
admin.site.register(Host,HostAdmin)
