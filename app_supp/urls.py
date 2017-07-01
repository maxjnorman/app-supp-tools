"""app_supp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^calendar/', include('app_supp_calendar.urls', namespace='calendar')),
    url(r'^', include('app_supp_global.urls', namespace='global')),
    url(r'^shifts/', include('app_supp_shifts.urls', namespace='shifts')),
    url(r'^teams/', include('app_supp_teams.urls', namespace='teams')),
    url(r'^upload/', include('app_supp_upload.urls', namespace='upload')),
    url(r'^users/', include('app_supp_users.urls', namespace='users')),
]
urlpatterns += [url(r'^accounts/', include('django.contrib.auth.urls'))]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
