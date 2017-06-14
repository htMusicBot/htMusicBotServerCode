# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170614_0622'),
    ]

    operations = [
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
                ('year', models.ForeignKey(to='main.Year', null=True)),
            ],
        ),
    ]
