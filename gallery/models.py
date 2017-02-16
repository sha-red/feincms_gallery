# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ungettext_lazy, ugettext_lazy as _

from feincms.module.medialibrary.models import MediaFile

from .specs.legacy import DEFAULT_SPECS


__all__ = ['Gallery', 'GalleryMediaFile', 'DEFAULT_SPECS']


@python_2_unicode_compatible
class Gallery(models.Model):
    internal_name = models.CharField(_("Interne Bezeichnung"), max_length=500, help_text=_("Erscheint nicht auf der Website"))
    title = models.CharField(_("Title"), max_length=500, null=True, blank=True)
    title_en = models.CharField(_("Title (english)"), max_length=500, null=True, blank=True)
    description_de = models.TextField(_("Description"), null=True, blank=True)
    description_en = models.TextField(_("Description (english"), null=True, blank=True)
    images = models.ManyToManyField(MediaFile, verbose_name=_("Gallery Images"), through='GalleryMediaFile')  # TODO Restrict to type='image'?
    
    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")

    def __str__(self):
        return self.internal_name

    def ordered_images(self):
        return self.images.select_related().all() \
            .order_by('gallerymediafile__ordering')
    
    def count_images(self):
        if not getattr(self, '_image_count', None):
            self._image_count = self.images.count()
        return self._image_count

    def verbose_images(self):
        count = self.count_images()
        return ungettext_lazy('%(count)d Image',
                              '%(count)d Images', count) % {'count': count}
    verbose_images.short_description = _("Image Count")
    

@python_2_unicode_compatible
class GalleryMediaFile(models.Model):
    gallery = models.ForeignKey(Gallery)
    mediafile = models.ForeignKey(MediaFile)
    ordering = models.IntegerField(default=9999)
    
    class Meta:
        verbose_name = 'Image for Gallery'
        verbose_name_plural = 'Images for Gallery'
        ordering = ['ordering']
        
    def __str__(self):
        return "%s" % self.mediafile
