from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dynamic.views import view_index

urlpatterns = patterns('',
     url(r'^$', view_index),
     url(r'^admin/', include(admin.site.urls)),
)
