# Generated by Django 4.1.4 on 2023-01-19 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adan', '0028_prayerevent_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='prayer_time_am_pm',
            field=models.JSONField(blank=True, null=True, verbose_name='prayer data time'),
        ),
    ]
