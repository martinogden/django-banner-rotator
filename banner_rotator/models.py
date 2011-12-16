#-*- coding:utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

#from django_extensions.db.fields import AutoSlugField

from banner_rotator.managers import BannerManager


class Campaign(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'))
    width = models.SmallIntegerField(_('Width'), blank=True, null=True, default=None)
    height = models.SmallIntegerField(_('Height'), blank=True, null=True, default=None)

    class Meta:
        unique_together = ('slug',)

    def __unicode__(self):
        return self.name

    def size_str(self):
        if self.width and self.height:
            return '%sx%s' % (self.width, self.height)
        elif self.width:
            return '%sxX' % self.width
        elif self.height:
            return 'Xx%s' % self.height
        else:
            return ''


class Banner(models.Model):
    URL_TARGET_CHOICES = (
        ('', _('Current page')),
        ('_blank', _('Blank page')),
    )

    campaign = models.ForeignKey(Campaign, verbose_name=_('Campaign'), blank=True, null=True, default=None,
        related_name="banners", db_index=True)

    name = models.CharField(_('Name'), max_length=255)
    alt = models.CharField(_('Image alt'), max_length=255, blank=True, default='')

    url = models.URLField(_('URL'))
    url_target = models.CharField(_('Target'), max_length=10, choices=URL_TARGET_CHOICES, default='')

    views = models.IntegerField(_('Views'), default=0)
    clicks = models.IntegerField(_('Clicks'), default=0)
    max_views = models.IntegerField(_('Max views'), default=0)
    max_clicks = models.IntegerField(_('Max clicks'), default=0)

    weight = models.IntegerField(_('Weight'), help_text=_("A ten will display 10 times more often that a one."),
        choices=[[i,i] for i in range(1, 11)])

    file = models.FileField(_('File'), upload_to='banners')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_at = models.DateTimeField(_('Start at'), blank=True, null=True, default=None)
    finish_at = models.DateTimeField(_('Finish at'), blank=True, null=True, default=None)

    is_active = models.BooleanField(_('Is active'), default=True)

    places = models.ManyToManyField(Place, verbose_name=_('Place'), related_name="banners", db_index=True)

    objects = BannerManager()

    def __unicode__(self):
        return self.name

    def is_swf(self):
        return self.file.name.lower().endswith("swf")

    def view(self):
        self.views = models.F('views') + 1
        self.save()
        return ''

    def click(self, request):
        self.clicks = models.F('clicks') + 1
        self.save()

        click = {
            'banner': self,
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'referrer': request.META.get('HTTP_REFERER'),
        }

        if request.user.is_authenticated():
            click['user'] = request.user

        return Click.objects.create(**click)

    @models.permalink
    def get_absolute_url(self):
        return ('banner_click', (), {'banner_id': self.pk})

    def admin_clicks_str(self):
        if self.max_clicks:
            return '%s / %s' % (self.clicks, self.max_clicks)
        return '%s' % self.clicks
    admin_clicks_str.short_description = _('Clicks')

    def admin_views_str(self):
        if self.max_views:
            return '%s / %s' % (self.views, self.max_views)
        return '%s' % self.views
    admin_views_str.short_description = _('Views')


class Click(models.Model):
    banner = models.ForeignKey(Banner, related_name="clicks_list")
    user = models.ForeignKey(User, null=True, blank=True, related_name="banner_clicks")
    datetime = models.DateTimeField("Clicked at", auto_now_add=True)
    ip = models.IPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)

