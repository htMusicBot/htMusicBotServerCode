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
            field=models.CharField(default=b'NULL', max_length=250, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='Name',
            field=models.CharField(default=b'NULL', max_length=250, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='lyricist',
            name='Name',
            field=models.CharField(default=b'NULL', max_length=250, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='moviename',
            name='Name',
            field=models.CharField(default=b'NULL', max_length=250, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='musicdirector',
            name='Name',
            field=models.CharField(default=b'NULL', max_length=250, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='Cast',
            field=models.ManyToManyField(to=b'main.Actor', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='Category',
            field=models.ForeignKey(to='main.Category', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='Lyricist',
            field=models.ManyToManyField(to=b'main.Lyricist', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='MovieName',
            field=models.ForeignKey(to='main.MovieName', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='MusicDirector',
            field=models.ManyToManyField(to=b'main.MusicDirector', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='Singer',
            field=models.ManyToManyField(to=b'main.Singer', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='SongName',
            field=models.CharField(default=b'NULL', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='YoutubeLink',
            field=models.CharField(default=b'NULL', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='year',
            field=models.ForeignKey(to='main.Year', null=True),
        ),
        migrations.AlterField(
            model_name='year',
            name='Year',
            field=models.CharField(default=b'NULL', max_length=250, unique=True, null=True),
        ),
    ]
