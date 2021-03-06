# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-04 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medialibrary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Galleries',
                'verbose_name': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='GalleryMediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.IntegerField(default=9999)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Gallery')),
                ('mediafile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medialibrary.MediaFile')),
            ],
            options={
                'verbose_name_plural': 'Images for Gallery',
                'verbose_name': 'Image for Gallery',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='gallery',
            name='images',
            field=models.ManyToManyField(through='gallery.GalleryMediaFile', to='medialibrary.MediaFile'),
        ),
    ]
