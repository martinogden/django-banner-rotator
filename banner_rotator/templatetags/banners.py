#-*- coding:utf-8 -*-

import logging

from django import template
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from banner_rotator.models import Banner, Place


logger = logging.getLogger('banner_rotator')

register = template.Library()


class BannerNode(template.Node):
    def __init__(self, place_slug, varname=None):
        self.varname, self.place_slug, = varname, place_slug

    def render(self, context):
        try:
            self.place = Place.objects.get(slug=self.place_slug)
        except Place.DoesNotExist:
            return ''

        local_context = {'banner_place': self.place}

        try:
            banner_obj = Banner.objects.biased_choice(self.place)
            banner_obj.view()
        except Banner.DoesNotExist:
            banner_obj = None

        local_context['banner'] = banner_obj

        if self.varname:
            context.update(local_context)
            return ''
        else:
            templates = [
                #'banner_rotator/place_%s.html' % banner_obj.place.slug,
                'banner_rotator/place.html'
            ]
            return render_to_string(templates, local_context)


@register.tag
def banner(parser, token):
    """
    Use: {% banner place-slug as banner %} or {% banner place-slug %}
    """
    bits = token.contents.split()

    if len(bits) not in [2, 4]:
        raise template.TemplateSyntaxError(_("banner tag takes three of four arguments"))

    if 4 == len(bits) and 'as' == bits[2]:
        place_slug = bits[1]
        varname = bits[3]
    else:
        place_slug = bits[1]
        varname = None

    return BannerNode(place_slug, varname)
