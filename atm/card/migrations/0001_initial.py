# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('number', models.CharField(verbose_name='number', unique=True, max_length=16)),
                ('pin', models.CharField(verbose_name='pin', max_length=4)),
                ('is_locked', models.BooleanField(verbose_name='is locked', default=False)),
                ('try_count', models.IntegerField(verbose_name='try count', default=0)),
                ('_balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='balance')),
            ],
            options={
                'verbose_name_plural': 'cards',
                'verbose_name': 'card',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('time', models.DateTimeField(verbose_name='time', auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, blank=True, verbose_name='amount', null=True)),
                ('code', models.CharField(verbose_name='code', max_length='10', choices=[('balance', 'check card balance'), ('cash_out', 'cash out')])),
                ('card', models.ForeignKey(to='card.Card', verbose_name='card', related_name='operations')),
            ],
            options={
                'verbose_name_plural': 'card operations',
                'verbose_name': 'card operation',
                'ordering': ['card', '-time'],
            },
        ),
    ]
