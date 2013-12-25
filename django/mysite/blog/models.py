from django.db import models
from django.contrib import admin

class BlogPost(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	timestamp = models.DateTimeField()

class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title','timestamp')

class Meta:
	ordering = ('-timestamp',)

admin.site.register(BlogPost,BlogPostAdmin)
