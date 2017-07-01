from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^team/(?P<pk>\d+)/manage-documents/$', views.manage_documents, name='manage_documents'),
    url(r'^file/(?P<pk>\d+)/upload/$', views.upload_file, name='upload_file'),
    url(r'^file/(?P<pk>\d+)/delete/$', views.delete_file, name='delete_file'),
    url(r'^file/(?P<pk>\d+)/deactivate/$', views.deactive_file, name='deactive_file'),
    url(r'^file/(?P<pk>\d+)/activate/$', views.active_file, name='active_file'),
]
