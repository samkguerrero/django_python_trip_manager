from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^login$', views.login),
    url(r'^trips/new$', views.new_trip),
    url(r'^trips/edit/(?P<trip_id>[0-9]+)$', views.edit_trip),
    url(r'^trips/join/(?P<trip_id>[0-9]+)$', views.join_trip),
    url(r'^trips/cancel/(?P<trip_id>[0-9]+)$', views.cancel_trip),
    url(r'^trips/(?P<trip_id>[0-9]+)$', views.show_trip),
]