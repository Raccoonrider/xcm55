# Generated by Django 5.0.3 on 2024-04-07 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_paymentwindow_options_paymentwindow_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='start_location',
            field=models.CharField(max_length=255, null=True, verbose_name='Место старта'),
        ),
    ]