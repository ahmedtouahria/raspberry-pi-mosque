# Generated by Django 4.1.4 on 2022-12-17 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adan', '0008_alter_prayerevent_prayer'),
    ]

    operations = [
        migrations.AddField(
            model_name='prayerevent',
            name='audio',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to='prayer_event'),
        ),
    ]
