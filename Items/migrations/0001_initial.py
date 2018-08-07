# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Items.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bidonitem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField(validators=[Items.utils.minimum_validator])),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bidding_time', models.DurationField(default=3600)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('starting_bid', models.PositiveIntegerField(validators=[Items.utils.minimum_validator])),
            ],
        ),
        migrations.AddField(
            model_name='bidonitem',
            name='item',
            field=models.ForeignKey(related_name='bids', to='Items.Item'),
        ),
    ]
