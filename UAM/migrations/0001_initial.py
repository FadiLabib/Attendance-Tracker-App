# Generated by Django 3.0.7 on 2020-06-29 16:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begun', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('expired', models.DateTimeField(default=django.utils.timezone.now)),
                ('subscribed', models.BooleanField(default=False)),
            ],
        ),
    ]
