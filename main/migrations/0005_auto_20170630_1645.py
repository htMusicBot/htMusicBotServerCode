# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170630_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='year',
        ),
        migrations.AddField(
            model_name='song',
            name='year',
            field=models.ForeignKey(to='main.Year', null=True),
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='year',
        ),
        migrations.AddField(
            model_name='userdata',
            name='year',
            field=models.ManyToManyField(to='main.Year', null=True),
        ),
    ]
