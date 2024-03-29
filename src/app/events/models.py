from django.db import models

from common.models import BaseViewableModel, BaseRelation, BaseModel
from common.enums import ResultStatus

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
        ordering = ('-active', '-created',)

    def __str__(self):
        return f"{self.name} {self.distance} км"


class Event(BaseViewableModel):
    date = models.DateField(
        null=False,
        verbose_name="Дата",
        )
    time = models.TimeField(
        null=True,
        verbose_name="Время старта",
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
    rules_doc = models.FileField(
        blank=True,
        verbose_name="Регламент",
        upload_to="event_rules"
    )
    finished = models.BooleanField()
    routes = models.ManyToManyField(
        to=Route,
        through='EventRoute'
    )

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

    class Meta:
        verbose_name = 'Связь "Маршрут-событие"'
        verbose_name_plural = 'Связь "Маршрут-событие"'


class Application(BaseModel):
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
    user_profile = models.ForeignKey(
        to='users.UserProfile',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Профиль пользователя"
    )
    payment_confirmed = models.BooleanField(
        default=False,
        verbose_name="Оплата прошла"
    )
    result = models.ForeignKey(
        to='events.Result',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Результат"
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


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
    user_profile = models.ForeignKey(
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
    status = models.IntegerField(
        default=ResultStatus.OK,
        choices=ResultStatus.choices(),
        verbose_name="Статус",
    )
    
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'