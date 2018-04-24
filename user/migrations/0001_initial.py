# Generated by Django 2.0.2 on 2018-04-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('chat_url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=150)),
                ('email', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(max_length=40)),
            ],
        ),
    ]