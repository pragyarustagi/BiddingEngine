# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0002_auto_20180725_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='bidding_time',
        ),
        migrations.AddField(
            model_name='item',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 27, 17, 2, 56, 534486)),
        ),
        migrations.AlterField(
            model_name='bidonitem',
            name='item',
            field=models.ForeignKey(related_name='bids', to='Items.item'),
        ),
    ]
