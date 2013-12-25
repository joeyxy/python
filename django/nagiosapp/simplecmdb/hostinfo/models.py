from django.db import models

class Host(models.Model):
	memory_size = models.CharField(max_length=30,null=True)
	hostname = models.CharField(max_length=30,null=True)
	ipaddr = models.IPAddressField(max_length=15)
	def __unicode__(self):
		return self.hostname

class HostGroup(models.Model):
	name = models.CharField(max_length=30)
	members =models.ManyToManyField(Host)
