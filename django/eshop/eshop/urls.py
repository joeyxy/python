from django.conf.urls import patterns, include, url
#from order.views import hello,current_datetime,hours_ahead,current_url,ua_display,display_meta
from django.views.generic.list import ListView
from order.views import *
from order.models import Publisher

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

publisher_info = {
    'queryset':Publisher.objects.all(),
    'template_name':'publisher_list_page.html',
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eshop.views.home', name='home'),
    # url(r'^eshop/', include('eshop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     (r'^hello/$',hello),
     #(r'^search-form/$',search_form),
     (r'^search/$',search),
     (r'^ua_display/$',ua_display),
     (r'^display_meta/$',display_meta),
     (r'^current_url/$',current_url),
     (r'^time/$',current_datetime),
     (r'^time/plus/(\d{1,2})/$',hours_ahead),
     (r'^publishers/$',ListView.as_view,publisher_info),

)
