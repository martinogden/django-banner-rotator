#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template

from banner_rotator.models import Banner


register = template.Library()

class BannerNode(template.Node):

    def __init__(self, varname='banner', campaign_slug=None):
        self.varname, self.campaign_slug = varname, campaign_slug

    def render(self, context):
        kwargs = {}
        if self.campaign_slug:
            kwargs['campaign__slug'] = self.campaign_slug
        try:
            banner = Banner.objects.biased_choice(**kwargs)
        except Banner.DoesNotExist:
            context[self.varname] = None
            return ''
        else:
            banner.view()
            context[self.varname] = banner
            return ''

@register.tag
def banner(parser, token):
    """
    Use: {% banner campaign-slug as banner %}

    Pick a banner using the biased / weighting manager, with an optional campaign slug
    """
    bits = token.contents.split()

    if len(bits) not in [3,4]:
        raise template.TemplateSyntaxError, "banner tag takes three of four arguments"

    if bits[2] == 'as':
        varname = bits[3]
        campaign = bits[1]
    else:
        varname = bits[2]
        campaign = None

    return BannerNode(varname, campaign)

class BannersNode(template.Node):

    def __init__(self, count, varname='banners', campaign_slug=None):
        self.varname, self.campaign_slug, self.count = varname, campaign_slug, count

    def render(self, context):
        kwargs = {}
        if self.campaign_slug:
            kwargs['campaign__slug'] = self.campaign_slug
        try:
            banners = Banner.objects.biased_sample(self.count, **kwargs)
        except Banner.DoesNotExist:
            context[self.varname] = None
            return ''
        else:
            for i in banners:
                i.view()
            context[self.varname] = banners
            return ''

@register.tag
def banners(parser, token):
    """
    Use: {% banners 3 campaign-slug as banners %}

    Pick a collection of banners using the biased / weighting manager, with an optional campaign slug
    """
    bits = token.contents.split()

    # banners, count, campaign, as, varname
    # 0,       1,     2,        3,  4
    # 1,       2,     3,        4,  5
    if len(bits) not in [3, 4, 5]:
        raise template.TemplateSyntaxError, "banner tag takes three of five arguments"

    if bits[3] == 'as':
        count = bits[1]
        campaign = bits[2]
        varname = bits[4]
    else:
        count = bits[1]
        campaign = bits[2]
        varname = bits[3]

    return BannersNode(count, varname, campaign)

