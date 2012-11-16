#-*- coding:utf-8 -*-

import logging

from django import forms, template
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.db import models
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode
from django.utils.functional import update_wrapper
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from banner_rotator.models import Campaign, Place, Banner, Click


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'size_str')
    prepopulated_fields = {'slug': ('name',)}


class CampaignBannerInline(admin.StackedInline):
    model = Banner
    extra = 0
    readonly_fields = ['views', 'clicks']
    fields = ['is_active', 'places', 'name', 'url', 'file', 'weight', 'views', 'clicks']
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    fields = ('name',)
    inlines = [CampaignBannerInline]


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'weight', 'url', 'views', 'is_active')
    list_filter = ('campaign', 'places', 'is_active')
    date_hierarchy = 'created_at'
    fieldsets = (
        (_('Main'), {
            'fields': ('campaign', 'places', 'name', 'url', 'url_target', 'file', 'alt'),
        }),
        (_('Show'), {
            'fields': ('weight', 'views', 'max_views', 'clicks', 'max_clicks', 'start_at', 'finish_at', 'is_active'),
        })
    )

    filter_horizontal = ('places',)
    readonly_fields = ('views', 'clicks',)

    object_log_clicks_template = None

    def get_urls(self):
        try:
            # Django 1.4
            from django.conf.urls import patterns, url
        except ImportError:
            from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info),
            url(r'^(.+)/history/$', wrap(self.history_view), name='%s_%s_history' % info),
            url(r'^(.+)/delete/$', wrap(self.delete_view), name='%s_%s_delete' % info),
            url(r'^(.+)/log/clicks/$', wrap(self.log_clicks_view), name='%s_%s_log_clicks' % info),
            url(r'^(.+)/$', wrap(self.change_view), name='%s_%s_change' % info),
        )
        return urlpatterns

    def log_clicks_view(self, request, object_id, extra_context=None):
        model = self.model
        opts = model._meta
        app_label = opts.app_label

        obj = get_object_or_404(model, pk=unquote(object_id))

        context = {
            'title': _('Log clicks'),
            'module_name': capfirst(force_unicode(opts.verbose_name_plural)),
            'object': obj,
            'app_label': app_label,
            'log_clicks': Click.objects.filter(banner=obj).order_by('-datetime')
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.object_log_clicks_template or [
            "admin/%s/%s/object_log_clicks.html" % (app_label, opts.object_name.lower()),
            "admin/%s/object_log_clicks.html" % app_label,
        ], context, context_instance=context_instance)


admin.site.register(Banner, BannerAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Place, PlaceAdmin)
