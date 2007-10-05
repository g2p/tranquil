from django.conf.urls.defaults import *

urlpatterns = patterns('proj_name.app_name.views',
	url(r'^$', 'index', name='root' ),
	url(r'^polls/$', 'index', name='index'),
	url(r'^polls/(?P<poll_id>\d+)/$', 'detail', name='detail'),
	url(r'^polls/(?P<poll_id>\d+)/results/$', 'results', name='results'),
	url(r'^polls/(?P<poll_id>\d+)/vote/(?P<choice_id>\d+)/$', 'vote', name='vote'),
	url(r'^admin/', include( 'django.contrib.admin.urls' ) ),
)
