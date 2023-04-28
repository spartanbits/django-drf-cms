# Generated by Django 4.2 on 2023-04-27 09:53

from django.db import migrations, models
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('drf_cms', '0002_alter_text_unique_together_remove_text_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='description_en',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='description_es',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='title_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='title_es',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='content_en',
            field=django_bleach.models.BleachField(null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='content_es',
            field=django_bleach.models.BleachField(null=True),
        ),
    ]
