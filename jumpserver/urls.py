from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    (r'^$', 'jumpserver.views.index'),
    (r'^api/user/$', 'jumpserver.api.api_user'),
    (r'^skin_config/$', 'jumpserver.views.skin_config'),
    (r'^install/$', 'jumpserver.views.install'),
    (r'^base/$', 'jumpserver.views.base'),
    (r'^login/$', 'jumpserver.views.login'),
    (r'^logout/$', 'jumpserver.views.logout'),
    (r'^file/upload/$', 'jumpserver.views.upload'),
    (r'^file/download/$', 'jumpserver.views.download'),
    (r'^error/$', 'jumpserver.views.httperror'),
    (r'^juser/', include('juser.urls')),
    (r'^jasset/', include('jasset.urls')),
    (r'^jlog/', include('jlog.urls')),
    (r'^jperm/', include('jperm.urls')),
    (r'^node_auth/', 'jumpserver.views.node_auth'),

)
