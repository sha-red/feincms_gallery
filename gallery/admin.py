# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.contrib import admin
from django.core.exceptions import FieldError
from django.http import (HttpResponse, HttpResponseRedirect,
    HttpResponseBadRequest, HttpResponseForbidden)
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.html import escapejs
from django.utils.translation import ugettext_lazy as _, ungettext
from django.views.decorators.csrf import csrf_exempt

from feincms.module.medialibrary.models import Category, MediaFile
from feincms.templatetags import feincms_thumbnail

from .forms import ThumbnailForm, MediaFileWidget
from .models import Gallery, GalleryMediaFile


# FIXME What are the consequences of this crsf_exempt?
@csrf_exempt
def admin_thumbnail(request):
    content = u''
    if request.method == 'POST' and request.is_ajax():
        form = ThumbnailForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors)
        data = form.cleaned_data

        obj = data['id']
        dimensions = '%sx%s' % (data['width'], data['height'])

        if obj.type == 'image':
            image = None
            try:
                image = feincms_thumbnail.thumbnail(obj.file.name, dimensions)
            except:
                pass

            if image:
                try:
                    caption = obj.translation.caption
                except AttributeError:
                    caption = _(u'untitled').encode('utf-8')
                content = json.dumps({
                    'url': image.url,
                    'name': escapejs(caption)
                })
        return HttpResponse(content, content_type='application/json')
    else:
        return HttpResponseForbidden()
admin_thumbnail.short_description = _("Image")
admin_thumbnail.allow_tags = True


class GalleryMediaFileAdminForm(forms.ModelForm):
    mediafile = forms.ModelChoiceField(
        queryset=MediaFile.objects.filter(type='image'),
        widget=MediaFileWidget(attrs={'class': 'image-fk'}), label=_('media file'))

    class Meta:
        model = GalleryMediaFile
        fields = ('gallery', 'mediafile', 'ordering')


class GalleryMediaFileAdmin(admin.ModelAdmin):
    model = GalleryMediaFile
    form = GalleryMediaFileAdminForm
    list_display = ['title', admin_thumbnail]
    classes = ['sortable']


class GalleryMediaFileInline(admin.StackedInline):
    model = GalleryMediaFile
    form = GalleryMediaFileAdminForm
    template = 'admin/gallery/gallery/stacked.html'
    raw_id_fields = ('mediafile',)
    extra = 0
    classes = ['sortable']
    ordering = ['ordering']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'verbose_images']
    fields = (
        ('title', 'title_en'),
        ('description_de', 'description_en'),
        'background_color',
    )
    inlines = [GalleryMediaFileInline]

    def assign_category(self, request, queryset):
        class AddCategoryForm(forms.Form):
            _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
            category = forms.ModelChoiceField(Category.objects)

        form = None
        if 'apply' in request.POST:
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                count = 0
                mediafiles = MediaFile.objects.filter(categories=category)
                for gallery in queryset:
                    for mediafile in mediafiles:
                        try:
                            GalleryMediaFile.objects.create(gallery=gallery, mediafile=mediafile)
                        except FieldError:
                            pass
                        count += 1
                message = ungettext('Successfully added %(count)d mediafiles in %(category)s Category.',
                                    'Successfully added %(count)d mediafiles in %(category)s Categories.', count) % {
                                        'count': count,
                                        'category': category}
                self.message_user(request, message)
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = AddCategoryForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render_to_response('admin/gallery/action_forms/add_category.html', {
            'mediafiles': queryset,
            'category_form': form}, context_instance=RequestContext(request))
    assign_category.short_description = _("Assign Images from a Category")

    actions = [assign_category]
