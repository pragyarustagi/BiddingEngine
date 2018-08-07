# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0003_auto_20180727_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='expected_amount',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 1, 12, 13, 12, 436643), null=True, blank=True),
        ),
    ]
