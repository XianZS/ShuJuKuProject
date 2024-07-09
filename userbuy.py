from django.db import models


class userbuy(models.Model):
    userbuyname = models.CharField(primary_key=True, max_length=32)
    userbuycount = models.IntegerField()
    first_userbuy_car = models.ForeignKey(to="car", to_field="carid", on_delete=models.SET_NULL, null=True,
                                          blank=True,
                                          related_name="first_userbuy_car")
    second_userbuy_car = models.ForeignKey(to="car", to_field="carid", on_delete=models.SET_NULL, null=True,
                                           blank=True,
                                           related_name="second_userbuy_car")
    third_userbuy_car = models.ForeignKey(to="car", to_field="carid", on_delete=models.SET_NULL, null=True,
                                          blank=True,
                                          related_name="third_userbuy_car")
    class Meta:
        verbose_name_plural = verbose_name = "个人所购票表"
