# Generated by Django 2.2 on 2020-09-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('loc_x', models.FloatField()),
                ('loc_y', models.FloatField()),
                ('made', models.BooleanField(default=True)),
                ('opponent', models.CharField(default='unspecified', max_length=200)),
                ('shot_type', models.CharField(default='unspecified', max_length=200)),
            ],
        ),
    ]
