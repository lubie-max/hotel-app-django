# Generated by Django 3.2.13 on 2022-05-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='location',
            field=models.CharField(default='Mumbai', max_length=200),
        ),
    ]
