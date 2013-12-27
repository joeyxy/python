from django.db import models
  
class Product(models.Model):  
	name = models.CharField('product name', max_length=30)  
	price = models.FloatField('price', default=10)  
	def __unicode__(self):  
		return "%s --> %f" %(self.name,self.price) 

class Publisher(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=60)
	state_province = models.CharField(max_length=30)
	country = models.CharField(max_length=50)
	website = models.URLField()
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Author(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=40)
	email = models.EmailField()

	def __unicode__(self):
		return u'%s %s' %(self.first_name,self.last_name)

class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField(Author)
	publisher = models.ForeignKey(Publisher)
	publication_date = models.DateField()

	def __unicode__(self):
		return self.title


