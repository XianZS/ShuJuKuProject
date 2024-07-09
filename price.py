"""
    @mian: models
    @somethings: price
    @note: 票价信息表
"""

from django.db import models


class price(models.Model):
    # 票价ID
    priceid = models.IntegerField(primary_key=True)
    # 售票情况，所剩多少张票
    nums = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"票价ID : {self.priceid};所剩容量 : {self.nums};价格 : {self.money}"

    class Meta:
        verbose_name_plural = verbose_name = "价格信息表"
