# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-30 21:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textquestion',
            name='tolerance',
        ),
    ]
