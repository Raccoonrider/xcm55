from datetime import date, time, timedelta
from secrets import token_hex
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
from segno import make_qr

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
    halfmarathon = models.BooleanField(
        default=False,
        verbose_name="Полумарафон"
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
    finished = models.BooleanField(
        default=False,
        verbose_name="Событие закончено",
    )
    registration_closed = models.BooleanField(
        default=False,
        verbose_name="Регистрация закрыта",
    )
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
    emegrency_phone_number = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Номер телефона для экстренной связи",
        help_text="Для печати на номерах",
    )
    result_qr = models.ImageField(
        null=True,
        blank=True,
        verbose_name="QR протокола",
        help_text="Для печати на номерах",
        upload_to='events/results_qr'
    )

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Cобытия"
    
    def get_display_name(self):
        return f"{self.name} - {self.date.year}"
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk':self.pk})
    
    def get_results_url(self):
        return reverse('event_results', kwargs={'pk':self.pk})
    
    def application_url(self):
        return reverse('application_create', kwargs={'pk':self.pk})
    
    def generate_result_qr(self):
        qr = make_qr(f"https://xcm55.ru{self.get_results_url()}")
        path = Path(settings.MEDIA_ROOT) / 'events' / 'results_qr'
        path.mkdir(parents=True, exist_ok=True)
        path = path / f'{token_hex(4)}.png'

        qr.save(str(path), scale=5)

        self.result_qr = str(path.relative_to(settings.MEDIA_ROOT))

    def save(self, *args, **kwargs):
        if not self.result_qr:
            self.generate_result_qr()
        super().save(*args, **kwargs)

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
    number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Номер",
    )

    def agegroup(self):
        age = self.user_profile.age(self.event.date)

        return AgeGroup.objects.filter(
            event=self.event, 
            gender=self.user_profile.gender,
            age_min__lte = age,
            age_max__gte = age,
            ).first()
        
    def autonumber(self):
        if self.number is not None:
            self.number = None
            self.save()

        if self.category == Category.Elite:
            number_min = 1
            number_max = 50
        
        elif self.route.halfmarathon == False:
            agegroup = self.agegroup()
            if agegroup is not None:
                number_min = agegroup.number_min
                number_max = agegroup.number_max
            else:
                number_min = 100
                number_max = 199
                    
        elif self.route.halfmarathon:
            number_min = 100
            number_max = 199
            
        used_numbers = {x.number for x in Application.objects.filter(event=self.event, active=True)}

        for n in range(number_min, number_max + 1):
            if n not in used_numbers:
                self.number = n
                self.save()
                return n

    def render_category(self):
        if self.category == Category.Elite:
            return "Элита"
        if self.category == Category.Junior:
            return "Юниоры"
        if self.route.halfmarathon == True:
            return "Полумарафон"
        if self.category == Category.Default:
            return str(self.agegroup())
        
    def render_number(self):
        return str(self.number)
    
    def render_background(self):
        age_group = self.agegroup()
        if age_group:
            return age_group.color
        else:
            return "#FFF"


    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def distance(self):
        return self.route.distance


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
    number = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Номер"
    )
    category = models.IntegerField(
        null=True,
        blank=True,
        choices=Category.choices(),
        verbose_name="Категория",
        default=Category.Default,
    )
    age_group = models.ForeignKey(
        to='events.AgeGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Возрастная группа"
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

    def render_time(self):
        if self.time:
            t = round(self.time.total_seconds())
            h, t = divmod(t, 3600)
            m, s = divmod(t, 60)

            return F"{h:02d}:{m:02d}:{s:02d} {self.render_status()}" 
        return f"--:--:-- {self.render_status()}"
    
    def render_status(self):
        if self.status == ResultStatus.OK:
            return ""
        return ResultStatus.name_int(self.status)
    
    def render_category(self):
        if self.category == Category.Elite:
            return "Элита"
        if self.category == Category.Junior:
            return "Юниоры"
        if self.route.halfmarathon == True:
            return "Полумарафон"
        if self.category == Category.Default:
            return str(self.age_group)

    def avg_speed(self):
        if self.time:
            return "{:.02f} км/ч".format(self.route.distance / self.time.total_seconds() * 3600)
        return "-"

    def __str__(self):
        return F"{self.number} | {self.render_time()}"



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
    number_min = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Номер участника, от"
    )
    number_max = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Номер участника, до"
    )
    gender = models.IntegerField(
        null=False,
        default=Gender.M,
        choices=Gender.choices(),
        verbose_name="Пол",
    )
    color = ColorField(
        default="#FFFFFF", 
        verbose_name="Цвет фона номера",
        )

    def birthday_min(self):
        return self.event.date.replace(year = self.event.date.year - self.age_max - 1) - timedelta(days=1)

    def birthday_max(self):
        return self.event.date.replace(year = self.event.date.year - self.age_min)

    def __str__(self):

        if self.age_max <= 13:
            if self.gender == Gender.M:
                gender = "Мальчики"
            else:
                gender = "Девочки"

        elif self.age_max <= 18:
            if self.gender == Gender.M:
                gender = "Юноши"
            else:
                gender = "Девушки"

        else:
            if self.gender == Gender.M:
                gender = "Мужчины"
            else:
                gender = "Женщины"

        if self.age_max == 100:
            return f"{gender} от {self.age_min} лет"
        
        return f"{gender} от {self.age_min} до {self.age_max} лет"
    
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