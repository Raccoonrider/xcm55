# Generated by Django 5.0.7 on 2024-07-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_alter_application_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='agegroup',
            name='number_max',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер участника, от'),
        ),
        migrations.AddField(
            model_name='agegroup',
            name='number_min',
            field=models.IntegerField(blank=True, null=True, verbose_name='Номер участника, до'),
        ),
    ]
