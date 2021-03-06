# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 11:38
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ja', models.CharField(max_length=255)),
                ('abstract', models.TextField()),
                ('abstract_ja', models.TextField()),
                ('link', models.TextField()),
                ('subject', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'papers',
            },
        ),
        migrations.CreateModel(
            name='RssFetchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'rss_fetch_histories',
            },
        ),
        migrations.CreateModel(
            name='RssFetchSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('url', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fetch_subjects',
            },
        ),
        migrations.AddField(
            model_name='rssfetchhistory',
            name='rss_fetch_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rss_fetch_histories', related_query_name='rss_fetch_history', to='app.RssFetchSubject'),
        ),
        migrations.AddField(
            model_name='paper',
            name='rss_fetch_history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', related_query_name='paper', to='app.RssFetchHistory'),
        ),
    ]
