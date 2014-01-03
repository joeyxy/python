from django.db import models

class Host(models.Model):
    vendor = models.CharField(max_length=30,null=True)
    sn = models.CharField(max_length=30,null=True)
    product = models.CharField(max_length=30,null=True)
    cpu_model = models.CharField(max_length=50,null=True)
    cpu_num = models.CharField(max_length=2,null=True)
    cpu_vendor = models.CharField(max_length=30,null=True)
    memory_part_number = models.CharField(max_length=30,null=True)
    memory_manufacturer = models.CharField(max_length=30,null=True)
    memory_size = models.CharField(max_length=30,null=True)
    device_model = models.CharField(max_length=30,null=True)
    device_version = models.CharField(max_length=30,null=True)
    device_sn = models.CharField(max_length=30,null=True)
    device_size = models.CharField(max_length=30,null=True)
    osver = models.CharField(max_length=30,null=True)
    hostname = models.CharField(max_length=30,null=True)
    os_release = models.CharField(max_length=30,null=True)
    ipaddr = models.IPAddressField(max_length=15)
    def __unicode__(self):
        return self.hostname


class HostGroup(models.Model):
	name = models.CharField(max_length=30)
	members =models.ManyToManyField(Host)
