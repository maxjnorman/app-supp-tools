from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)/detail/$', views.team_detail, name='team_detail'),
    url(r'^(?P<pk>\d+)/edit/membership/$', views.edit_membership, name='edit_membership'),
    url(r'^(?P<team_pk>\d+)/manager/add/(?P<profile_pk>\d+)/$', views.add_manager, name='add_manager'),
    url(r'^(?P<team_pk>\d+)/manager/remove/(?P<profile_pk>\d+)/$', views.remove_manager, name='remove_manager'),
    url(r'^(?P<team_pk>\d+)/member/add/(?P<profile_pk>\d+)/$', views.add_member, name='add_member'),
    url(r'^(?P<team_pk>\d+)/member/remove/(?P<profile_pk>\d+)/$', views.remove_member, name='remove_member'),
]
