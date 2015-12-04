# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moive_posts', '0004_post_rate_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(max_length=1, choices=[(b'0', b'biography'), (b'1', b'agriculture'), (b'2', b'crime'), (b'3', b'arts'), (b'4', b'energy'), (b'5', b'sports'), (b'6', b'science'), (b'7', b'history')]),
        ),
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=models.ImageField(upload_to=b'static/'),
        ),
    ]
