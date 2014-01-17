from django.db import models

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
    def __unicode__(self):
        return u'time:%s app:%s update:%s' %(self.time,self.appname,self.update)

class UpdateLog(models.Model):
    time = models.DateField()
    zone = models.ForeignKey(Zone)
    publicip = models.IPAddressField()
    privateip = models.IPAddressField()
    status = models.CharField(max_length=50)



class OperatingSystem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Admin:
        pass

class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Admin:
        pass

class HardwareComponent(models.Model):
    manufacturer = models.CharField(max_length=50)
    #types include video card, network card...
    type = models.CharField(max_length=50)
    model = models.CharField(max_length=50, blank=True, null=True)
    vendor_part_number = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.manufacturer

    class Admin:
        pass

class Location(models.Model):
    location = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.location

    class Admin:
        pass


class Server(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    os = models.ForeignKey(OperatingSystem)
    location = models.ForeignKey(Location)
    services = models.ManyToManyField(Service)
    hardware_component = models.ManyToManyField(HardwareComponent)
    def __str__(self):
        return self.name

    class Admin:
        pass


class IPAddress(models.Model):
    address = models.TextField(blank=True, null=True)
    server = models.ForeignKey(Server)

    def __str__(self):
        return self.address

    class Admin:
        pass
