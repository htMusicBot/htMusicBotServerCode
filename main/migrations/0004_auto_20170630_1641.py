# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userdata_query'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='year',
        ),
        migrations.AddField(
            model_name='song',
            name='year',
            field=models.ManyToManyField(to='main.Year', null=True),
        ),
    ]
