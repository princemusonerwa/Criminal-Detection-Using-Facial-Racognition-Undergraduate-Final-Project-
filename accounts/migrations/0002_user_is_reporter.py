# Generated by Django 3.1.5 on 2021-02-22 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_reporter',
            field=models.BooleanField(default=True),
        ),
    ]
