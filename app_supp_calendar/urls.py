from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^month/(?P<pk>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.month_view, name='month_view'),
    url(r'^week/(?P<pk>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.week_view, name='week_view'),
    url(r'^day/(?P<pk>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', views.day_view, name='day_view'),
]
