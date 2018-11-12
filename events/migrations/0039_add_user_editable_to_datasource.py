# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-15 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from django.conf import settings


def forward(apps, schema_editor):
    DataSource = apps.get_model('events', 'DataSource')
    try:
        system_data_source = DataSource.objects.get(id=settings.SYSTEM_DATA_SOURCE_ID)
        system_data_source.user_editable = True
        system_data_source.save()
    except DataSource.DoesNotExist:
        pass




class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_add_index_for_last_modified_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='user_editable',
            field=models.BooleanField(default=False, verbose_name='Objects may be edited by users'),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_systems', to='events.Organization'),
        ),
        migrations.RunPython(forward, migrations.RunPython.noop)
    ]
