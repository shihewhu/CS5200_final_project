# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('moive_posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 29, 0, 45, 51, 352000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poster',
            name='image',
            field=models.ImageField(default=datetime.datetime(2015, 11, 29, 0, 45, 58, 612000, tzinfo=utc), upload_to=b''),
            preserve_default=False,
        ),
    ]
