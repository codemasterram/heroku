# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0004_hastag'),
    ]

    operations = [
        migrations.AddField(
            model_name='hastag',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
