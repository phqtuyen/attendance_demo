# Generated by Django 2.0.2 on 2018-04-24 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=255)),
                ('messageid', models.CharField(max_length=255)),
                ('roomid', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttendanceSubmit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('correct_submission', models.BooleanField()),
                ('attendance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendance_app.Attendance')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RocketAPIAuthentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rocket_chat_user_id', models.CharField(max_length=100)),
                ('rocket_chat_auth_token', models.CharField(max_length=150)),
                ('rocket_chat_url', models.CharField(max_length=255)),
            ],
        ),
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
        migrations.AddField(
            model_name='attendancesubmit',
            name='submitted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendance_app.UserProfile'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='attendance_app.UserProfile'),
        ),
    ]
