# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moive_posts', '0002_auto_20151128_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rate',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
    ]
