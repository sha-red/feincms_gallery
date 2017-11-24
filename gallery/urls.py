from django.conf.urls import include, url

from gallery.admin import admin_thumbnail


urlpatterns = [
    url(r'^thumbnail/$', admin_thumbnail, name='gallery_admin_thumbnail'),
]
