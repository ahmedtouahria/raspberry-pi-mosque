# Generated by Django 4.1.4 on 2023-01-02 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adan', '0020_prayeraudio_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mosque',
            name='topic',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='adan.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
