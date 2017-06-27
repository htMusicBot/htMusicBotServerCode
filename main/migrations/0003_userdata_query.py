# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userdata_cast'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='query',
            field=models.ManyToManyField(to='main.Song', null=True),
        ),
    ]
