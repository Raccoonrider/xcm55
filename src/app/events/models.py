from django.db import models

from common.models import BaseViewableModel, make_path


class Series(BaseViewableModel):
    pass


class Route(BaseViewableModel):
    distance = models.IntegerField(
        verbose_name="Дистанция",
        )
    map_embed_src = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Ссылка на карту",
        ) 
    gpx = models.FileField(
        upload_to=make_path("gpx"), 
        blank=True, 
        verbose_name="*.gpx",
        )
    series = models.ForeignKey(
        to=Series,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )    


class Event(BaseViewableModel):
    date = models.DateField(
        null=False,
        verbose_name="Дата",
        )
    time = models.TimeField(
        null=True,
        verbose_name="Время старта",
    )
    route = models.ForeignKey(
        to=Route,
        on_delete=models.CASCADE,
    )
    series = models.ForeignKey(
        to=Series,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )    
    vk_xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка ВК",
        )
    finished = models.BooleanField()
    
    
    def get_display_name(self):
        return f"{self.name} - {self.date.year}"