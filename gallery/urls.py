# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from .admin import admin_thumbnail


urlpatterns = [
    url(r'^thumbnail/$', admin_thumbnail, name='gallery_admin_thumbnail'),
]
