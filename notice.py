from django.db import models


class notice(models.Model):
    # 主题
    topic = models.CharField(max_length=30, default="无主题")
    # 内容
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name_plural = verbose_name = "公告"
