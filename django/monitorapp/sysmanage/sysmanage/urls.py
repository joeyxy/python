from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sysmanage.views.home', name='home'),
    # url(r'^sysmanage/', include('sysmanage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'inventory.views.main'),
    (r'^categorized/(?P<category>.*?)/(?P<category_id>.*?)/$', 'inventory.views.categorized'),
    (r'^server_detail/(?P<server_id>.*?)/$','inventory.views.server_detail'),
    (r'^server_list/$','inventory.views.server_list'),

)
