# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-15 08:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0002_articlecomments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomments',
            name='comments',
            field=models.TextField(verbose_name='评论'),
        ),
    ]
