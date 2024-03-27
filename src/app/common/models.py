from pathlib import Path
from uuid import uuid4
import re


from django.db import models

from common.shortcuts import transliterate


def make_path(prefix:str):
    """Makes upload path with a given prefix"""
    def wrapper(instance, filename):
        suffix = Path(filename).suffix

        if hasattr(instance, 'name') and instance.name:
            name = instance.name
        elif hasattr(instance, 'slug') and instance.slug:
            name = instance.slug
        elif hasattr(instance, 'series') and instance.series:
            name = instance.series.name
        else:
            name = uuid4()
        if hasattr(instance, 'date') and instance.date:
            name = f"{instance.date.year}_{name}"

        name = re.sub(r"[^\w ]", "", name)
        name = re.sub(r" +", "_", name)

        return f"{prefix}/{name}{suffix}"
    return wrapper


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    saved = models.DateTimeField(auto_now=True)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True


class BaseViewableModel(BaseModel):
    name = models.CharField(
        max_length=200, 
        verbose_name="Название",
        ) 
    slug = models.SlugField(
        blank=True,
        )
    brief = models.TextField(
        blank=True, 
        verbose_name='Краткое описание',
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание',
        )
    image = models.ImageField(
        null=True,
        upload_to=make_path(prefix="img"), 
        blank=True, 
        verbose_name="Картинка",
        )
    
    class Meta:
        abstract = True

    def get_display_name(self):
        return self.name