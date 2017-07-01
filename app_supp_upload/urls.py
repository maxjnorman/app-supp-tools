from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^team/(?P<pk>\d+)/manage-documents/$', views.manage_documents, name='manage_documents'),
]
