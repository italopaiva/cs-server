# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 03:37
from __future__ import unicode_literals

import codeschool.lms.activities.models.activity
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code', '0003_auto_20170505_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codequestion',
            name='disabled',
            field=models.BooleanField(
                default=bool, help_text='Activities can be automatically disabled when Codeshool encounters an error. This usually produces a message saved on the .disabled_message attribute. This field is not controlled directly by users.', verbose_name='Disabled'),
        ),
        migrations.AlterField(
            model_name='codequestion',
            name='visible',
            field=models.BooleanField(default=codeschool.lms.activities.models.activity.bool_to_true,
                                      help_text='Makes activity invisible to users.', verbose_name='Invisible'),
        ),
    ]
