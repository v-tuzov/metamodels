from django.conf.urls.defaults import *
  
urlpatterns = patterns('dynamic.views',

    (r'^$', 'view_index')
    )