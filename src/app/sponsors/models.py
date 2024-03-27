from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseViewableModel, make_path

class Sponsor(BaseViewableModel):
    xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка на сайт",
    )
    vk_xref = models.URLField(
        blank=True, 
        verbose_name="Ссылка ВК",
    )
    phone = PhoneNumberField(
        null=True, 
        blank=True
    )