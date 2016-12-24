from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register_process$' , views.register_process),
	url(r'^login_process$' , views.login_process),
	# url(r'^users/(?P<id>\d+)$' , views.users),
	url(r'^success$' , views.success),
	url(r'^new_trip$' , views.new_trip),
	url(r'^add_trip$' , views.add_trip),
	url(r'^join_trip/(?P<id>\d+)$' , views.join_trip),
	url(r'^unjoin_trip/(?P<id>\d+)$' , views.unjoin_trip),
	url(r'^user/(?P<id>\d+)$' , views.user),
	url(r'^destination/(?P<id>\d+)$' , views.destination),
	# # url(r'^remove_fav/(?P<id>\d+)$' , views.remove_fav),
	url(r'^logout$', views.logout)

]
