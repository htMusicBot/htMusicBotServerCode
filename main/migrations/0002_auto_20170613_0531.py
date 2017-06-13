# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SongName', models.CharField(default=b'NULL', max_length=250)),
                ('YoutubeLink', models.CharField(default=b'NULL', max_length=250)),
            ],
        ),
        migrations.RenameModel(
            old_name='Cast',
            new_name='Actor',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='Cast',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='Category',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='Lyricist',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='MovieName',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='MusicDirector',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='Singer',
        ),
        migrations.RemoveField(
            model_name='songs',
            name='year',
        ),
        migrations.AddField(
            model_name='moviename',
            name='Cast',
            field=models.CharField(default=b'NULL', max_length=250),
        ),
        migrations.DeleteModel(
            name='Songs',
        ),
        migrations.AddField(
            model_name='song',
            name='Cast',
            field=models.ManyToManyField(to='main.Actor'),
        ),
        migrations.AddField(
            model_name='song',
            name='Category',
            field=models.ForeignKey(to='main.Category'),
        ),
        migrations.AddField(
            model_name='song',
            name='Lyricist',
            field=models.ManyToManyField(to='main.Lyricist'),
        ),
        migrations.AddField(
            model_name='song',
            name='MovieName',
            field=models.ForeignKey(to='main.MovieName'),
        ),
        migrations.AddField(
            model_name='song',
            name='MusicDirector',
            field=models.ManyToManyField(to='main.MusicDirector'),
        ),
        migrations.AddField(
            model_name='song',
            name='Singer',
            field=models.ManyToManyField(to='main.Singer'),
        ),
        migrations.AddField(
            model_name='song',
            name='year',
            field=models.ForeignKey(to='main.Year'),
        ),
    ]
