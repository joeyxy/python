from django.contrib import admin
from models import *

admin.site.register(OperatingSystem)
admin.site.register(Service)
admin.site.register(HardwareComponent)
admin.site.register(Server)
admin.site.register(IPAddress)
admin.site.register(Location)
admin.site.register(UpdateLog)
admin.site.register(VersionList)
admin.site.register(ServerList)
admin.site.register(Zone)

