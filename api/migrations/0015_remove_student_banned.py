# Generated by Django 3.1.1 on 2021-02-17 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210217_2250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='banned',
        ),
    ]
