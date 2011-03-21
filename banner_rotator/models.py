from django.db import models

from adto.managers import BiasedManager


class Campaign(models.Model):

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Banner(models.Model):

    objects = BiasedManager()

    campaign = models.ForeignKey("adto.Campaign")

    name = models.CharField(max_length=255)
    url = models.URLField()

    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    weight = models.IntegerField(help_text="A ten will display 10 times more often that a one.",\
        choices=[[i,i] for i in range(11)])

    image = models.ImageField(upload_to='uploads/banners')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def click(self):
        self.clicks += 1
        self.save()
        return self.clicks

    def view(self):
        self.impressesion +=1
        self.save()
        return self.impressions

    @models.permalink
    def get_absolute_url(self):
        return ('banner_click', (), {'banner_id': self.pk})
