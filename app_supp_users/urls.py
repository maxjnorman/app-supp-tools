from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^profile/create/$', views.create_profile, name='create_profile'),
    url(r'^admin/$', views.user_admin, name='user_admin'),
    url(r'^edit/(?P<pk>\d+)/$', views.user_edit, name='user_edit'),
    url(r'^admin/profile/(?P<team_pk>\d+)/create/(?P<user_pk>\d+)/$', views.admin_profile_create, name='admin_profile_create'),
    url(r'^admin/user/(?P<team_pk>\d+)/create/$', views.admin_user_create, name='admin_user_create'),
    url(r'^(?P<user_pk>\d+)/detail/$', views.user_detail, name='user_detail'),
]
