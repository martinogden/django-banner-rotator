#-*- coding:utf-8 -*-

import logging

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from banner_rotator.models import Campaign, Place, Banner


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'size_str')
admin.site.register(Place, PlaceAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(Campaign, CampaignAdmin)


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign', 'place', 'weight', 'url', 'views', 'is_active')
    list_filter = ('campaign', 'place', 'is_active')
    date_hierarchy = 'created_at'
    fieldsets = (
        (_('Main'), {
            'fields': ('campaign', 'place', 'name', 'url', 'url_target', 'file', 'alt'),
        }),
        (_('Show'), {
            'fields': ('weight', 'max_views', 'max_clicks', 'start_at', 'finish_at', 'is_active'),
        })
    )

admin.site.register(Banner, BannerAdmin)


#class CampaignAdmin(admin.ModelAdmin):
#    inlines = [BannerAdminInline]
#
#admin.site.register(Campaign, CampaignAdmin)
#
#
#class BannerForm(forms.ModelForm):
#    """
#    We override the form to add the click count as a 'hidden' field,
#        Field is a textinput, and looks invisible due to css styling.
#
#    This is a little hacky but it's an easy workaround, and isn't public facing
#    """
#    clicks = forms.CharField(required=False, widget=forms.TextInput(
#        attrs={'readonly':'readonly', 'style':'border: none; padding: 0;'}))
#
#    class Meta:
#        model = Banner
#
#    def __init__(self, *args, **kwargs):
#        super(BannerForm, self).__init__(*args, **kwargs)
#
#        # Set the form fields based on the model object
#        if kwargs.has_key('instance'):
#            instance = kwargs['instance']
#            self.initial['clicks'] = instance.clicks.count()
#        else:
#            self.initial['clicks'] = 0
#
#
#class BannerAdminInline(admin.StackedInline):
#    model = Banner
#    form = BannerForm
#    extra = 0
#    readonly_fields = ['views',]
#    fields = ['is_active', 'name', 'url', 'file', 'weight', 'clicks', 'views']
