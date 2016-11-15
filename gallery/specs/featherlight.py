# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2016
"""
Featherlight Based Gallery

https://github.com/noelboss/featherlight/#featherlight-gallery
"""

from django.utils.translation import ugettext_lazy as _
from .base import BaseSpec


class FeatherlightGallery(BaseSpec):
    verbose_name = _("Featherlight Lightbox Gallery")
    paginated = False
    template_name = 'featherlight.html'
    name = 'featherlight'

    media = {
        'css': {'all': ('js/vendor/featherlight/featherlight.min.css',
                        'js/vendor/featherlight/featherlight.gallery.min.css')},
        'js': ('js/vendor/featherlight/featherlight.min.js',
               'js/vendor/featherlight/featherlight.gallery.min.js'),
    }
