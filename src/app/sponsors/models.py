from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseViewableModel, BaseRelation

class Sponsor(BaseViewableModel):
    xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка на сайт",
    )
    vk_xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка ВК",
    )
    phone_number = PhoneNumberField(
        null=True, 
        blank=True
    )
    image = models.ImageField(
        null=False,
        blank=False, 
        upload_to='sponsor_logo', 
        verbose_name="Лого",
        )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Профиль спонсора"
        verbose_name_plural = "Профили спонсоров"


class EventSponsor(BaseRelation):
    event = models.ForeignKey(
        to='events.Event',
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