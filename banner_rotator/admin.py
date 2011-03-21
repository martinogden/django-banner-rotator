from django.contrib import admin

from adto.models import Campaign, Banner


class BannerAdminInline(admin.StackedInline):
    model = Banner
    extra = 1
    readonly_fields = ['impressions', 'clicks']


class CampaignAdmin(admin.ModelAdmin):
    inlines = [BannerAdminInline]

admin.site.register(Campaign, CampaignAdmin)
