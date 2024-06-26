from django.db import models
from django.urls import reverse

from common.models import BaseViewableModel, BaseRelation, BaseModel
from common.enums import ResultStatus, Category, Gender
from common.shortcuts import render_date

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
    start_location = models.CharField(
        null=True,
        verbose_name="Место старта",
        max_length=255,
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
    payment_info = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name="Номер карты",
    )
    routes = models.ManyToManyField(
        to=Route,
        through='EventRoute'
    )
    sponsors = models.ManyToManyField(
        to='sponsors.Sponsor',
        through='sponsors.EventSponsor'
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Cобытия"
    
    def get_display_name(self):
        return f"{self.name} - {self.date.year}"
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk':self.pk})

    
    def application_url(self):
        return reverse('application_create', kwargs={'pk':self.pk})
        

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
    category = models.IntegerField(
        null=False,
        blank=False,
        choices=Category.choices(),
        verbose_name="Категория"
    )
    helmet_not_needed = models.BooleanField(
        default=True,
        verbose_name="Буду в своём шлеме",
        help_text="Если у Вас нет своего шлема, его можно будет взять напрокат на старте. Снимите эту галочку, чтобы мы знали, что он Вам понадобится."
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
    referral = models.ForeignKey(
        to='sponsors.Referral',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рефералка",
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


class AgeGroup(models.Model):
    event = models.ForeignKey(
        to=Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Событие",
    )
    age_min = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Возраст, от"
    )
    age_max = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Возраст, до"
    )
    gender = models.IntegerField(
        null=False,
        default=Gender.M,
        choices=Gender.choices()
    )

    
    class Meta:
        verbose_name = 'Возрастная группа'
        verbose_name_plural = 'Возрастные группы'


class PaymentWindow(models.Model):
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
    price = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Цена",
    )
    active_until = models.DateField(
        null=False,
        blank=False,
        verbose_name="Доступна до"
    )
    
    class Meta:
        verbose_name = 'Интервал оплаты'
        verbose_name_plural = 'Интервалы оплаты'
        ordering = ('active_until',)

    def render_price(self):
        return f"{self.price}\u20bd"
    
    def render_date(self):
        return render_date(self.active_until)