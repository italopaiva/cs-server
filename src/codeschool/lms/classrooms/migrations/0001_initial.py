# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-15 00:49
from __future__ import unicode_literals

import codeschool.lms.classrooms.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0003_auto_20170615_0046'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(help_text='Classroom name', max_length=64, verbose_name='name')),
                ('slug', models.SlugField(help_text='Unique short name used on URLs.', primary_key=True, serialize=False, verbose_name='Short name')),
                ('weekly_lessons', models.BooleanField(default=False, help_text='If true, the lesson spans a whole week. Otherwise, each lesson would correspond to a single day/time slot.', verbose_name='weekly lessons')),
                ('accept_subscriptions', models.BooleanField(default=True, help_text='Set it to false to prevent new student subscriptions.', verbose_name='accept subscriptions')),
                ('is_public', models.BooleanField(default=True, help_text='If true, all students will be able to see the contents of the course. Most activities will not be available to non-subscribed students.', verbose_name='is it public?')),
                ('subscription_passphrase', models.CharField(blank=True, default=codeschool.lms.classrooms.models.random_subscription_passphase, help_text='A passphrase/word that students must enter to subscribe in the course. Leave empty if no passphrase should be necessary.', max_length=140, verbose_name='subscription passphrase')),
                ('short_description', models.CharField(help_text='A short one-sentence description used in listings.', max_length=140, verbose_name='short description')),
                ('description', wagtail.wagtailcore.fields.RichTextField(help_text='Long and detailed description.', verbose_name='Description')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.Course')),
                ('discipline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.Discipline')),
                ('staff', models.ManyToManyField(blank=True, related_name='classrooms_as_staff', to=settings.AUTH_USER_MODEL, verbose_name='staff')),
                ('students', models.ManyToManyField(blank=True, related_name='classrooms_as_student', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='classrooms_as_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
