from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'catmapper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', 'map.views.main', name='main'),
    url(r'^(?P<wiki_id>\d+)/save/?', 'map.views.save', name='save'),
    url(r'^(?P<wiki_id>\d+)/p/(?P<categories>.*)/?', 'map.views.pages', name='pages'),
    url(r'^(?P<wiki_id>\d+)/d/(?P<page_id>\d+)/?', 'map.views.details', name='details'),
    url(r'^(?P<wiki_id>\d+)/g/(?P<group_id>\d+)/?', 'map.views.group_details', name='group_details'),
    url(r'^(?P<wiki_id>\d+)/g/?', 'map.views.groups', name='groups'),
    url(r'^(?P<wiki_id>\d+)/?', 'map.views.main', name='main'),


    url(r'^admin/', include(admin.site.urls)),
)
