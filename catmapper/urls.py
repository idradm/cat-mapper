from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'catmapper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^', 'map.views.main', name='main'),
    url(r'^(?P<wiki_id>\d+)/save/?', 'map.views.save', name='save'),
    url(r'^(?P<wiki_id>\d+)/p/(?P<category>.*)/?', 'map.views.pages', name='pages'),
    url(r'^(?P<wiki_id>\d+)/?', 'map.views.main', name='main'),


    url(r'^admin/', include(admin.site.urls)),
)
