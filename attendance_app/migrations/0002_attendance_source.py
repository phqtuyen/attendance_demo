# Generated by Django 2.0.2 on 2018-04-23 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='source',
            field=models.CharField(default='', max_length=255),
        ),
    ]
