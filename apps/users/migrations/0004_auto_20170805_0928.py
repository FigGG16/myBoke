# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-05 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170804_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='is_useful',
            field=models.BooleanField(default=True),
        ),
    ]
