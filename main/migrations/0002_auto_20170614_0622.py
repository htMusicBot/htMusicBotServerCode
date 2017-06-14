# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='Name',
            field=models.CharField(default=b'NULL', unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='Name',
            field=models.CharField(default=b'NULL', unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lyricist',
            name='Name',
            field=models.CharField(default=b'NULL', unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='moviename',
            name='Name',
            field=models.CharField(default=b'NULL', unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='musicdirector',
            name='Name',
            field=models.CharField(default=b'NULL', unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='song',
            name='SongName',
            field=models.CharField(default=b'NULL', max_length=250),
        ),
        migrations.AlterField(
            model_name='year',
            name='Year',
            field=models.CharField(default=b'NULL', unique=True, max_length=250),
        ),
    ]
