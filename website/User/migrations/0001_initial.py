# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=64)),
                ('passwd', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('signature', models.CharField(default=b'This guy is very lazy to leave anything here', max_length=128)),
                ('photo', models.CharField(default=b'default.png', max_length=256)),
                ('is_login', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('salt', models.CharField(max_length=256)),
            ],
        ),
    ]
