# Generated by Django 5.0.3 on 2024-03-29 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_result_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventSponsor',
        ),
    ]
