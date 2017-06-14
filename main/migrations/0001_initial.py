# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Lyricist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='MovieName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='MusicDirector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SongName', models.CharField(default=b'NULL', max_length=250)),
                ('YoutubeLink', models.CharField(default=b'NULL', max_length=250, null=True)),
                ('Cast', models.ManyToManyField(to='main.Actor', null=True)),
                ('Category', models.ManyToManyField(to='main.Category', null=True)),
                ('Lyricist', models.ManyToManyField(to='main.Lyricist', null=True)),
                ('MovieName', models.ForeignKey(to='main.MovieName', null=True)),
                ('MusicDirector', models.ManyToManyField(to='main.MusicDirector', null=True)),
                ('Singer', models.ManyToManyField(to='main.Singer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Fbid', models.CharField(max_length=250)),
                ('State', models.CharField(default=b'NULL', max_length=250)),
                ('Category', models.ManyToManyField(to='main.Category', null=True)),
                ('Lyricist', models.ManyToManyField(to='main.Lyricist', null=True)),
                ('MovieName', models.ForeignKey(to='main.MovieName', null=True)),
                ('Singer', models.ManyToManyField(to='main.Singer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Year', models.CharField(default=b'NULL', unique=True, max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='userdata',
            name='year',
            field=models.ForeignKey(to='main.Year', null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='year',
            field=models.ForeignKey(to='main.Year', null=True),
        ),
    ]
