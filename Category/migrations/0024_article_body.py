# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-25 18:06
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0023_remove_article_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='body',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
    ]
