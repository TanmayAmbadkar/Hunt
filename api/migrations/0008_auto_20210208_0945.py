# Generated by Django 3.1.1 on 2021-02-08 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210208_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='finish',
            field=models.IntegerField(default=0),
        ),
    ]
