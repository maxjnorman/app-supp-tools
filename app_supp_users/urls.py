from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^/profile/create/$', views.create_profile, name='create_profile'),
    url(r'^/admin/$', views.user_admin, name='user_admin'),
    url(r'^/edit/(?P<pk>\d+)/$', views.user_edit, name='user_edit'),
]
