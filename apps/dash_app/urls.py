from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),

    url(r'^signin$', views.signin),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^registration$', views.registration),
    url(r'^show/user/(?P<user_id>\d+)$', views.wall),
    url(r'^message/(?P<user_id>\d+)$', views.process_message),
    url(r'^comment/(?P<user_id>\d+)$', views.process_comment),
    url(r'^shift/(?P<user_id>\d+)$', views.delta_wall),
    url(r'^dashboard$', views.showdash),
    url(r'^dashboard/admin$', views.admindash),
    url(r'^users/edit$', views.edit),
    url(r'^edit$', views.process_edit),
    url(r'^users/remove/(?P<user_id>\d+)$', views.remove),
    url(r'^remove/(?P<user_id>\d+)$', views.delete),
    url(r'^users/edit/(?P<user_id>\d+)$', views.edit_admin),
    url(r'^edit/admin/(?P<user_id>\d+)$', views.process_admin_edit),
    url(r'^users/new$', views.new),
    url(r'^add$', views.process_add),
    url(r'^logout$', views.logout),

]
