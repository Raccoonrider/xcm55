# Generated by Django 5.0.7 on 2024-08-08 17:48

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_event_payment_url_alter_event_payment_qr'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='payment_spb_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='ФИО для оплаты по СБП'),
        ),
        migrations.AddField(
            model_name='event',
            name='payment_spb_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон для оплаты по СБП'),
        ),
    ]
