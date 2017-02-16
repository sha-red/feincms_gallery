# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django import template
from django.db.models.query import QuerySet


register = template.Library()


@register.filter
def randomize(values):
    if not isinstance(values, QuerySet):
        if isinstance(values, list):
            return random.shuffle(values)
        return values
    return values.order_by('?')
