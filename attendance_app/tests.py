
from django.test import TestCase

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
#from django.core.urlresolvers import reverse
from attendance_app.views import AppViews
from attendance_app.models import UserProfile, Attendance, AttendanceSubmit
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
import requests

class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
    	self.tempProfile = UserProfile()
    	self.tempProfile.configID("a", "localhost")	\
    		.configName("first", "last")	\
    		.configEmail("email@gmail.com", "teacher")	\

    def test_temp_profile(self):
    	self.assertEqual(self.tempProfile.username, "a")
    	self.assertEqual(self.tempProfile.chat_url, "localhost")

    def test_create_profile(self):
    	userProfile = UserProfile.objects.createUserProfile(self.tempProfile)
    	self.assertEqual(len(UserProfile.objects.all()),1)

    def test_create_attendance(self):
    	userProfile = UserProfile.objects.createUserProfile(self.tempProfile)
    	attendance = Attendance.objects.createAttendance(userProfile,
    															timezone.now())	
    	att = Attendance.objects.getAttendanceByID(1)
    	self.assertEqual(att.id,attendance)

    def test_attendance_submit(self): 
    	userProfile = UserProfile.objects.createUserProfile(self.tempProfile)
    	attendance =  Attendance.objects.createAttendance(userProfile,
    															timezone.now())
    	att = Attendance.objects.getAttendanceByID(attendance)
    	att_submit = AttendanceSubmit.objects.createAttendanceSubmit(att, userProfile)
    	self.assertNotEqual(att_submit, 0)
    	self.assertNotEqual(att_submit, None)
    	subList = AttendanceSubmit.objects.getSubmissionList(att)
    	self.assertEqual(len(subList),1)														 

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist."""
        

        


