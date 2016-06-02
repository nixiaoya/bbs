# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('summary', models.CharField(max_length=258, null=True, blank=True)),
                ('content', models.TextField()),
                ('viewCount', models.IntegerField(default=0)),
                ('commentCount', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('chinese_name', models.CharField(unique=True, max_length=32)),
                ('father_category', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=256)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('vote', models.IntegerField(default=0)),
                ('article', models.ForeignKey(to='main.Article')),
                ('author', models.ForeignKey(to='users.User')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='main.Category'),
        ),
    ]
