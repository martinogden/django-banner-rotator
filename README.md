README
======

Приложение для ротации баннеров.

* Позволяет отслеживать количество кликов и просмотров.
* Поддерживает вес баннера, баннеры с большим весом чаще показываются.
* Есть возможность создавать рекламные компании.


Установка
======

Загрузите код из git репозитория:
    
    git clone git://github.com/plazix/django-banner-rotator.git django-banner-rotator
    
И добавте папку django-banner-rotator/banner_rotator в ваш PYTHONPATH.

Отредактируйте settings.py:

    INSTALLED_APPS = (

        "banner_rotator",

    )

Добавьте в urls.py:

    urlpatterns = patterns('',

        url(r'^banner_rotator/', include('banner_rotator.urls')),

    )

Добавьте в шаблон:

    {% load banners %}
    {% banner place-slug %}

или

    {% load banners %}
    {% banner place-slug as banner %}
    <a href="{% url banner_click banner.id %}?place_slug=place-slug"><img src="{{ banner.file.url }}" alt=""/></a>

