#-*- coding:utf-8 -*-

from random import random
from decimal import Decimal

from django.db import models


def pick(bias_list):
    """
    Takes a list similar to [(item1, item1_weight), (item2, item2_weight),]
        and item(n)_weight as the probability when calculating an item to choose
    """

    # All weights should add up to 1
    #   an items weight is equivalent to it's probability of being picked
    assert sum(i[1] for i in bias_list) == 1

    # Django ORM returns floats as Decimals,
    #   so we'll convert floats to decimals here to co-operate
    number = Decimal("%.18f" % random())
    current = Decimal(0)

    # With help from
    #   @link http://fr.w3support.net/index.php?db=so&id=479236
    for choice, bias in bias_list:
        current += bias
        if number <= current:
            return choice


class BannerManager(models.Manager):
    def biased_choice(self, place):
        queryset = self.filter(is_active=True, places=place)

        if not queryset.count():
            raise self.model.DoesNotExist

        calculations = queryset.aggregate(weight_sum=models.Sum('weight'))

        banners = queryset.extra(select={'bias': 'weight/%f' % calculations['weight_sum']})

        return pick([(b, b.bias) for b in banners])
