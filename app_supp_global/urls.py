from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^gloabal/landing_page/$', views.landing_page, name='landing_page'),
]
