from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djproject.views.home', name='home'),
    # url(r'^djproject/', include('djproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/', include('django.contrib.admin.urls.admin')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
