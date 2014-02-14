from django.contrib import admin
from models import *

admin.site.register(UpdateLog)
admin.site.register(VersionList,VersionListAdmin)
admin.site.register(ServerList)
admin.site.register(Zone)

