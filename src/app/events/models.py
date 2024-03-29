from django.db import models

from common.models import BaseViewableModel, BaseRelation, BaseModel


class Series(BaseViewableModel):
    pass

    class Meta:
        verbose_name = "Серия соревнований"
        verbose_name_plural = "Cерии соревнований"


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
        upload_to="gpx", 
        blank=True, 
        verbose_name="Трек *.gpx",
        )
    series = models.ForeignKey(
        to=Series,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Серия соревнований"
    )    

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Mаршруты"



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

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Cобытия"
    
    def get_display_name(self):
        return f"{self.name} - {self.date.year}"
        

class EventRoute(BaseRelation):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    route = models.ForeignKey(
        to=Route,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Маршрут"
    )
    route_category = models.CharField(
        null=False, 
        blank=False, 
        max_length=255, 
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = 'Связь "Маршрут-событие"'
        verbose_name_plural = 'Связь "Маршрут-событие"'


class EventSponsor(BaseRelation):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    sponsor = models.ForeignKey(
        to='sponsors.Sponsor',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Спонсор",
    )

    class Meta:
        verbose_name = 'Связь "Спонсор-событие"'
        verbose_name_plural = 'Связь "Спонсор-событие"'


class Result(BaseModel):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    route = models.ForeignKey(
        to=Route,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Маршрут"
    )
    user = models.ForeignKey(
        to='users.UserProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Профиль пользователя"
    )
    time = models.DurationField(
        null=True,
        blank=True,
        verbose_name="Время"
    )
    OTL = models.BooleanField(
        default=False,
        verbose_name="OTL (over time limit)"
    )
    DNF = models.BooleanField(
        default=False,
        verbose_name="DNF (did not finish)"
    )
    DSQ = models.BooleanField(
        default=False,
        verbose_name="DSQ (disqualified)"
    )
    
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'