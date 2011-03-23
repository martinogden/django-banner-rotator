from django.db import models

from banner_rotator.managers import BiasedManager


class Campaign(models.Model):

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Banner(models.Model):

    objects = BiasedManager()

    campaign = models.ForeignKey(Campaign, related_name="banners")

    name = models.CharField(max_length=255)
    url = models.URLField()

    impressions = models.IntegerField(default=0)

    weight = models.IntegerField(help_text="A ten will display 10 times more often that a one.",\
        choices=[[i,i] for i in range(11)])

    image = models.ImageField(upload_to='uploads/banners')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def view(self):
        self.impressesions = models.F('impressesions') + 1
        self.save()
        return self.impressions

    def click(self, request):
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


class Click(models.Model):

    banner = models.ForeignKey(Banner, related_name="clicks")
    user = models.ForeignKey("auth.User", null=True, blank=True, related_name="clicks")

    datetime = models.DateTimeField("Clicked at",auto_now_add=True)
    ip = models.IPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
