# Generated by Django 3.1.1 on 2020-12-27 07:55

import datetime
import detect.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('gender', models.CharField(max_length=255)),
                ('dob', models.DateField(null='True', verbose_name='Date of Birth')),
                ('address', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('NT', 'NOT WANTED'), ('W', 'WANTED')], default='NOT WANTED', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='detect.person')),
                ('staff_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            bases=('detect.person',),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ImageField(upload_to=detect.models.get_upload_to)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detect.person')),
            ],
        ),
        migrations.CreateModel(
            name='DetectedCriminal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('location', models.CharField(max_length=255)),
                ('person', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='detect.person')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detect.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('UI', 'Under Investigation'), ('SO', 'Solved')], default='Under Investigation', max_length=100)),
                ('person', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='detect.person')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='detect.person')),
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='detect.department')),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='detect.faculty')),
            ],
            bases=('detect.person',),
        ),
    ]
