#coding=utf-8
from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import models
from django.template import TemplateDoesNotExist
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ungettext_lazy, ugettext_lazy as _

from feincms.module.medialibrary.models import MediaFile

from .specs import DEFAULT_SPECS


class Gallery(models.Model):
    title = models.CharField(max_length=30)
    images = models.ManyToManyField(MediaFile, through='GalleryMediaFile')
    
    def ordered_images(self):
        return self.images.select_related().all().order_by('gallerymediafile__ordering')
    
    def count_images(self):
        return self.images.all().count()
    
    def verbose_images(self):
        count = self.count_images()
        return ungettext_lazy('%(count)d Image', '%(count)d Images', count) % {
                                                'count': count,}
    verbose_images.short_description = _('Image Count')
    
    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')
    
    def __unicode__(self):
        return self.title
    

class GalleryMediaFile(models.Model):
    gallery = models.ForeignKey(Gallery)
    mediafile = models.ForeignKey(MediaFile)
    ordering = models.IntegerField(default=9999)
    
    class Meta:
        verbose_name = 'Image for Gallery'
        verbose_name_plural = 'Images for Gallery'
        ordering = ['ordering']
        
    def __unicode__(self):
        return u'%s' %self.mediafile


class GalleryContent(models.Model):
    @classmethod
    def initialize_type(cls, specs=DEFAULT_SPECS, **kwargs):
        if 'feincms.module.medialibrary' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured, 'You have to add \'feincms.module.medialibrary\' to your INSTALLED_APPS before creating a %s' % cls.__name__

        cls.specs = dict([ ('%s_%s' % (spec.name, specs.index(spec)), spec) for spec in specs ])
        cls.spec_choices = [ (spec, cls.specs[spec].verbose_name ) for spec in cls.specs ]

        cls.add_to_class('type', models.CharField(max_length=20, choices=cls.spec_choices, default=cls.spec_choices[0][0]))
        
    gallery = models.ForeignKey(Gallery, \
        help_text=_('Choose a gallery to render here'),
        related_name='%(app_label)s_%(class)s_gallery')

    @property
    def spec(self):
        return self.specs[self.type]

    @property
    def media(self):
        return forms.Media(**self.spec.media)
      
    def has_pagination(self):
        return self.spec.paginated
        
    class Meta:
        abstract = True
        verbose_name = _('Image Gallery')
        verbose_name_plural = _('Image Galleries')


    def render(self, request, **kwargs):
        objects = self.gallery.ordered_images()
        remaining = []

        # check if the type is paginated
        if self.has_pagination():
            paginator = Paginator(objects, self.spec.paginate_by, orphans=self.spec.orphans)
            try:
                page = int(request.GET.get('page', 1))
            except ValueError:
                page = 1
            try:
                current_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                current_page = paginator.page(paginator.num_pages)

            images = current_page.object_list

            for object in objects:
                if object not in images:
                    remaining.append(object)
        else:
            current_page, paginator = None, None
            images = objects

        print self.spec.templates

        return render_to_string(self.spec.templates, {'content': self, 'block':current_page,
                'images': images, 'paginator': paginator,
                'remaining': remaining },
            context_instance = RequestContext(request))
