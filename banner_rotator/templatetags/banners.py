from django import template

from banner_rotator.models import Banner

register = template.Library()


class BannerNode(template.Node):

    def __init__(self, varname='banner', campaign_id=None):
        self.varname, self.campaign_id = varname, campaign_id

    def render(self, context):
        kwargs = {}
        if self.campaign_id:
            kwargs['campaign'] = self.campaign_id
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
    Use: {% banner 1 as banner %}

    Pick a banner using the biased / weighting manager, with an optional campaign number
    """
    bits = token.contents.split()

    if len(bits) not in [3,4]:
        raise template.TemplateSyntaxError, "pick_banner tag takes three of four arguments"
    
    if bits[2] == 'as':
        varname = bits[3]
        campaign = int(bits[1])
    else:
        varname = bits[2]
        campaign = None

    return BannerNode(varname, campaign)
