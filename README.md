README
======

Banner Rotation App for Django.

* Tracks clicks and views.
* Supports the weight of the banner, banners with large weight are shown more often.
* You can create ad campaigns.


Setup
======

Get the code via git:

    git clone git://github.com/martinogden/django-banner-rotator.git django-banner-rotator

Add the django-banner-rotator/banner_rotator folder to your PYTHONPATH.

Edit to settings.py:

    INSTALLED_APPS = (

        "banner_rotator",

    )

Edit to urls.py:

    urlpatterns = patterns('',

        url(r'^banner_rotator/', include('banner_rotator.urls')),

    )

Add the template:

    {% load banners %}
    {% banner place-slug %}

or

    {% load banners %}
    {% banner place-slug as banner %}
    <a href="{% url banner_click banner.id %}?place_slug=place-slug"><img src="{{ banner.file.url }}" alt=""/></a>

