# Generated by Django 5.0.7 on 2024-07-25 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_application_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]