from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^template/create/(?P<pk>\d+)/$', views.template_create, name='template_create'),
    url(r'^template/edit/(?P<pk>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/calendar/$',
        views.template_edit_calendar,
        name='template_edit_calendar'
    ),
    url(r'^template/deactivate/(?P<pk>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/calendar/$',
        views.template_deactivate_calendar,
        name='template_deactivate_calendar'
    ),
    url(r'^template/activate/(?P<pk>\d+)/$', views.template_activate, name='template_activate'),
    url(r'^template/deactivate/(?P<pk>\d+)/$', views.template_deactivate, name='template_deactivate'),
    url(r'^template/delete/(?P<pk>\d+)/$', views.template_delete, name='template_delete'),
    url(r'^template/edit/(?P<pk>\d+)/$', views.template_edit, name='template_edit'),
]
