# Generated by Django 5.0.7 on 2025-04-05 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0005_alter_referral_referral_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='general',
            field=models.BooleanField(default=False, help_text='Показывать этого спонсора на главной', verbose_name='Генеральный'),
        ),
    ]
