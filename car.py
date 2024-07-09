"""
    @mian: models
    @somethings: car
    @note: 汽车信息表
"""
from django.db import models


class car(models.Model):
    # 汽车id 主键
    carid = models.IntegerField(primary_key=True)
    # 汽车种类 A/B/C/D/E/F/G/H/I
    types = models.CharField(max_length=32)
    # 最大容量
    volume = models.IntegerField()
    # 汽车_线路ID 外键 参照road表的主键 --> roadid
    car_road = models.ForeignKey(to="road", to_field="roadid", on_delete=models.CASCADE, related_name="car_road")
    # 汽车_价格 外键 参照price表的主键 --> priceid
    car_price = models.ForeignKey(to="price", to_field="priceid", on_delete=models.CASCADE, related_name="car_price")

    def __str__(self) -> str:
        return f"汽车ID : {self.carid};汽车种类 : {self.types};最大容量 : {self.volume}"

    class Meta:
        verbose_name_plural = verbose_name = "汽车信息表"
