from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'user_add_item$', views.user_add_item),
    url(r'user_edit_item$', views.user_edit_item),
    url(r'user_delete_item/(?P<trip_id>[0-9]+)$', views.user_delete_item),
]