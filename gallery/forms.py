# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from feincms.module.medialibrary.models import MediaFile
from feincms.templatetags import feincms_thumbnail


class MediaFileWidget(forms.TextInput):
    """
    TextInput widget, shows a link to the current value if there is one.
    """

    def render(self, name, value, attrs=None):
        inputfield = super(MediaFileWidget, self).render(name, value, attrs)
        if value:
            try:
                mf = MediaFile.objects.get(pk=value)
            except MediaFile.DoesNotExist:
                return inputfield

            try:
                caption = mf.translation.caption
            except (ObjectDoesNotExist, AttributeError):
                caption = _('(no caption)')

            if mf.type == 'image':
                image = feincms_thumbnail.thumbnail(mf.file.name, '188x142')
                image = u'background: url(%(url)s) center center no-repeat;' % {'url': image}
            else:
                image = u''

            return mark_safe(u"""
                <div style="%(image)s" class="admin-gallery-image-bg absolute">
                <p class="admin-gallery-image-caption absolute">%(caption)s</p>
                %(inputfield)s</div>""" % {
                    'image': image,
                    'caption': caption,
                    'inputfield': inputfield})

        return inputfield


class ThumbnailForm(forms.Form):
    id = forms.ModelChoiceField(
        queryset=MediaFile.objects.filter(type='image')
    )
    width = forms.IntegerField(min_value=0)
    height = forms.IntegerField(min_value=0)

