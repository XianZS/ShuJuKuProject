"""
    @mian: models
    @somethings: road
    @note: 线路信息表
"""
from django.db import models
from datetime import datetime


class road(models.Model):
    # 线路ID 被参照属性
    roadid = models.IntegerField(primary_key=True)
    # 出发地
    begin = models.CharField(max_length=32)
    # 目的地
    ends = models.CharField(max_length=32)
    # year(4)+month(2)+day(2)+Hours(2)+minutes(2)+seconds(2)=14
    # 开始时间
    begintime = models.DateTimeField(default=datetime.today())
    # 所需时间
    needtime = models.IntegerField()

    def __str(self) -> str:
        return f"线路ID : {self.roadid} ; 出发地 : {self.begin} ; 目的地 : {self.ends} ; 开始时间 : {self.begintime} ; 所需时间 : {self.needtime}"

    class Meta:
        verbose_name_plural = verbose_name = "线路信息表"
