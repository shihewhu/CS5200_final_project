# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moive_posts', '0004_post_rate_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(max_length=1, choices=[(b'1', b'biography'), (b'2', b'agriculture'), (b'3', b'crime'), (b'4', b'arts'), (b'5', b'energy'), (b'6', b'sports'), (b'7', b'science'), (b'8', b'history')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='rate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=models.ImageField(upload_to=b'static/'),
        ),
    ]
