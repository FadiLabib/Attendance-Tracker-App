# Generated by Django 3.0.7 on 2020-07-01 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tracker', '0003_auto_20200630_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentattn',
            name='present',
            field=models.BooleanField(default=False),
        ),
    ]
