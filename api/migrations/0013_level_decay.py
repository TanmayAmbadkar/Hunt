# Generated by Django 3.1.1 on 2021-02-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='decay',
            field=models.FloatField(default=0.05, null=True),
        ),
    ]
