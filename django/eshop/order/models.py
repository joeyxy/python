from django.db import models
  
class Product(models.Model):  
	name = models.CharField('product name', max_length=30)  
	price = models.FloatField('price', default=10)  
	def __unicode__(self):  
		return "%s --> %f" %(self.name,self.price) 

# Create your models here.
