# Generated by Django 5.0.3 on 2024-04-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_result_dnf_remove_result_dsq_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='helmet_not_needed',
            field=models.BooleanField(default=True, help_text='Если у Вас нет своего шлема, его можно будет взять напрокат на старте. Снимите эту галочку, чтобы мы знали, что он Вам понадобится.', verbose_name='Буду в своём шлеме'),
        ),
    ]
