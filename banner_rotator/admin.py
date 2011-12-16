#-*- coding:utf-8 -*-

import logging

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from banner_rotator.models import Campaign, Place, Banner


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'size_str')


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


# todo добавить возможность просматривать список переходов по баннеру

class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'weight', 'url', 'admin_views_str', 'admin_clicks_str', 'is_active')
    list_filter = ('campaign', 'places', 'is_active')
    date_hierarchy = 'created_at'
    fieldsets = (
        (_('Main'), {
            'fields': ('campaign', 'places', 'name', 'url', 'url_target', 'file', 'alt'),
        }),
        (_('Show'), {
            'fields': ('weight', 'max_views', 'max_clicks', 'start_at', 'finish_at', 'is_active'),
        })
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }


admin.site.register(Banner, BannerAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Place, PlaceAdmin)
