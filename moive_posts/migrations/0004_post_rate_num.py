# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moive_posts', '0003_post_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rate_num',
            field=models.IntegerField(default=0),
        ),
    ]
