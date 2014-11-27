#-*- coding:utf-8 -*-

try:
    from hashlib import md5
except ImportError:
    from md5 import md5
from time import time
import six

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils.translation import ugettext_lazy as _

from banner_rotator.managers import BannerManager


def get_banner_upload_to(instance, filename):
    """
    Формирует путь для загрузки файлов
    """
    filename_parts = filename.split('.')
    ext = '.%s' % filename_parts[-1] if len(filename_parts) > 1 else ''
    if six.PY3:
        filename_str = ('%s-%s' % (filename, time())).encode('utf-8')
    else:
        filename_str = u'%s-%s' % (filename.encode('utf-8'), time())
    new_filename = md5(filename_str).hexdigest()
    return 'banner/%s%s' % (new_filename, ext)


class Campaign(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    created_at = models.DateTimeField(_('Create at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name = _('campaign')
        verbose_name_plural = _('campaigns')

    def __unicode__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'))
    width = models.SmallIntegerField(_('Width'), blank=True, null=True, default=None)
    height = models.SmallIntegerField(_('Height'), blank=True, null=True, default=None)

    class Meta:
        unique_together = ('slug',)
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __unicode__(self):
        size_str = self.size_str()
        return '%s (%s)' % (self.name, size_str) if size_str else self.name

    def size_str(self):
        if self.width and self.height:
            return '%sx%s' % (self.width, self.height)
        elif self.width:
            return '%sxX' % self.width
        elif self.height:
            return 'Xx%s' % self.height
        else:
            return ''
    size_str.short_description = _('Size')


class Banner(models.Model):
    URL_TARGET_CHOICES = (
        ('_self', _('Current page')),
        ('_blank', _('Blank page')),
    )

    campaign = models.ForeignKey(Campaign, verbose_name=_('Campaign'), blank=True, null=True, default=None,
        related_name="banners", db_index=True)

    name = models.CharField(_('Name'), max_length=255)
    alt = models.CharField(_('Image alt'), max_length=255, blank=True, default='')

    url = models.URLField(_('URL'))
    url_target = models.CharField(_('Target'), max_length=10, choices=URL_TARGET_CHOICES, default='')

    views = models.IntegerField(_('Views'), default=0)
    max_views = models.IntegerField(_('Max views'), default=0)
    max_clicks = models.IntegerField(_('Max clicks'), default=0)

    weight = models.IntegerField(_('Weight'), help_text=_("A ten will display 10 times more often that a one."),
        choices=[[i, i] for i in range(1, 11)], default=5)

    file = models.FileField(_('File'), upload_to=get_banner_upload_to)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_at = models.DateTimeField(_('Start at'), blank=True, null=True, default=None)
    finish_at = models.DateTimeField(_('Finish at'), blank=True, null=True, default=None)

    is_active = models.BooleanField(_('Is active'), default=True)

    places = models.ManyToManyField(Place, verbose_name=_('Place'), related_name="banners", db_index=True)

    objects = BannerManager()

    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banners')

    def __unicode__(self):
        return self.name

    def is_swf(self):
        return self.file.name.lower().endswith("swf")

    def view(self):
        self.views = models.F('views') + 1
        self.save()
        return ''

    def click(self, request):
        click = {
            'banner': self,
            'place': place,
            'ip': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'referrer': request.META.get('HTTP_REFERER'),
        }

        if request.user.is_authenticated():
            click['user'] = request.user

        return Click.objects.create(**click)

    @models.permalink
    def get_absolute_url(self):
        return 'banner_click', (), {'banner_id': self.pk}

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
    banner = models.ForeignKey(Banner, related_name="clicks")
    user = models.ForeignKey(User, null=True, blank=True, related_name="banner_clicks")
    datetime = models.DateTimeField("Clicked at", auto_now_add=True)
    ip = models.IPAddressField(null=True, blank=True)
    user_agent = models.TextField(validators=[MaxLengthValidator(1000)], null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
