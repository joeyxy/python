from django.conf.urls.defaults import *
from items.models import Item,Photo
from django.views.generic import RedirectView

urlpatterns = patterns('django.views.generic',
   url(r'^$',RedirectView.as_view,
        kwargs={
            'template':'index.html',
            'extra_context':{'item_list':lambda:Item.objects.all()}
        },
        name='index'
   ),
   url(r'^items/(?P<object_id>\d+)/$','list_detail.object_detail',
        kwargs={
            'queryset':Item.objects.all(),
            'template_name':'items_detail.html'
        },
        name='item_detail'
   ),
   url(r'^photos/(?P<object_id>\d+)/$','list_detail.object_detail',
        kwargs={
            'queryset':Photo.objects.all(),
            'template_name':'photos_detail.html'
        },
        name='photo_detail'
   ),
)
