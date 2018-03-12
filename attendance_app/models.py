from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length = 150)
    chat_url = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    email = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    role = models.CharField(max_length = 40)

class Attendance(models.Model):
	created_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
	created_on = models.DateTimeField(auto_now_add = True)

class AttendanceSubmit(models.Model):
	attendance = models.ForeignKey(Attendance, on_delete = models.SET_NULL, null = True)
	submitted_on = models.DateTimeField(auto_now_add = True)	
	submitted_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)


