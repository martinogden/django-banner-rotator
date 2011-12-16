#!/usr/bin/env python

from setuptools import setup, find_packages

from banner_rotator import get_version


setup(name='django-banner-rotator',
    version=get_version().replace(' ', '-'),
    description='Banner Rotation App for Django',
    author='Martin Ogden',
    url='http://github.com/martinogden/django-banner-rotator',
    include_package_data = True,
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)

