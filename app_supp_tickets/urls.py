from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^file/(?P<pk>\d+)/process/$', views.map_docfile, name='map_docfile'),
]
