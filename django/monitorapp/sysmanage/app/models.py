from django.db import models
from django.contrib import admin

# Create your models here.

class Zone(models.Model):
    name = models.CharField(max_length=50)
    platform = models.CharField(max_length=20)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class ServerList(models.Model):
    publicip = models.IPAddressField()
    privateip = models.IPAddressField()
    appname = models.CharField(max_length=50)
    apppath = models.CharField(max_length=50)
    zone = models.ForeignKey(Zone)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.appname


class VersionList(models.Model):
    appname = models.ForeignKey(ServerList)
    zonelist = models.ManyToManyField(Zone)
    time = models.DateField()
    md5 = models.CharField(max_length=50)
    update = models.BooleanField()
    def __str__(self):
        return self.appname

class VersionListAdmin(admin.ModelAdmin):
    list_display = ('appname','time','md5','update')

class UpdateLog(models.Model):
    time = models.DateField()
    zone = models.ForeignKey(Zone)
    publicip = models.IPAddressField()
    privateip = models.IPAddressField()
    status = models.CharField(max_length=50)
