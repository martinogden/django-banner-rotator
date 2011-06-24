import logging

from django.contrib import admin
from django import forms

from banner_rotator.models import Campaign, Banner

class BannerForm(forms.ModelForm):
    """
    We override the form to add the click count as a 'hidden' field,
        Field is a textinput, and looks invisible due to css styling.

    This is a little hacky but it's an easy workaround, and isn't public facing
    """
    clicks = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'readonly':'readonly', 'style':'border: none; padding: 0;'}))

    class Meta:
        model = Banner

    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)

        # Set the form fields based on the model object
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['clicks'] = instance.clicks.count()
        else:
            self.initial['clicks'] = 0


class BannerAdminInline(admin.StackedInline):
    model = Banner
    form = BannerForm
    extra = 0
    readonly_fields = ['impressions',]
    fields = ['is_active', 'name', 'url', 'image', 'weight', 'clicks', 'impressions']


class CampaignAdmin(admin.ModelAdmin):
    inlines = [BannerAdminInline]

admin.site.register(Campaign, CampaignAdmin)
