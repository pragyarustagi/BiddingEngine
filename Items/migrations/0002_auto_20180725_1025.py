# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidonitem',
            name='user',
            field=models.ForeignKey(related_name='bidded_on', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='product_name',
            field=models.CharField(default=None, max_length=15),
            preserve_default=False,
        ),
    ]
