# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20170627_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='user',
            name='cost',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='mpg',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
