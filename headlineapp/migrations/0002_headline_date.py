# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('headlineapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 29, 7, 11, 37, 141901, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
