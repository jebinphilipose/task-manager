# Generated by Django 3.1.2 on 2020-10-24 07:49

import api.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201022_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=api.models.DateTimeWithoutTZField(db_index=True),
        ),
    ]
