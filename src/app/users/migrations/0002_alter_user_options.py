# Generated by Django 5.0.3 on 2024-03-29 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Аккаунт', 'verbose_name_plural': 'Аккаунты'},
        ),
    ]
