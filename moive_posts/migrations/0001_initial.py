# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_content', models.CharField(max_length=4000)),
                ('date_posted', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('director_name', models.CharField(max_length=200)),
                ('cast', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=1, choices=[(b'0', b'biograhpy'), (b'1', b'agriculture'), (b'2', b'crime'), (b'3', b'arts'), (b'4', b'energy'), (b'5', b'sports'), (b'6', b'science'), (b'7', b'history')])),
                ('description', models.CharField(max_length=4000)),
                ('production_company', models.CharField(max_length=200)),
                ('release_region', models.CharField(max_length=200)),
                ('author', models.ForeignKey(related_name='author_name', to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'list of user', through='moive_posts.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(to='moive_posts.Post')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_to',
            field=models.ForeignKey(to='moive_posts.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commented_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
