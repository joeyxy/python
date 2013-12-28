from django.conf.urls.defaults import *

#from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', 'logview.views.list_files'),
    (r'^viewlog/(?P<sortmethod>.*?)/(?P<filename>.*?)/$', 'logview.views.view_log'),
 #   url(r'^admin/', include(admin.site.urls)),

)
