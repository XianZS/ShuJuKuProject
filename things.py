from django.db import models


class things(models.Model):
    # 留言的客户账号
    namethings = models.CharField(max_length=20)
    # 留言内容
    saythings = models.TextField(max_length=500)

    class Meta:
        verbose_name_plural = verbose_name = "客户留言"
