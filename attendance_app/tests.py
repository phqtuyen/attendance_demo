
from django.test import TestCase
from django.test import Client
# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
#from django.core.urlresolvers import reverse
from attendance_app.views import AppViews
from attendance_app.models import UserProfile, Attendance, AttendanceSubmit
from attendance_app.networks import RocketUsersAPI
from attendance_app.networks import RocketSettingSandBox

from django.http import HttpResponse, HttpRequest
from django.utils import timezone
import requests

# class ModelTestCase(TestCase):
#     """This class defines the test suite for the bucketlist model."""

#     def setUp(self):
#     	self.tempProfile = UserProfile()
#     	self.tempProfile.configID("a", "localhost")	\
#     		.configName("first", "last")	\
#     		.configEmail("email@gmail.com", "teacher")	\

#     def test_temp_profile(self):
#         self.assertEqual(self.tempProfile.username, "a")
#         self.assertEqual(self.tempProfile.chat_url, "localhost")
#         self.assertEqual(self.tempProfile.role, "teacher")

#     def test_create_profile(self):
#     	userProfile = UserProfile.objects.createUserProfile(self.tempProfile)
#     	self.assertEqual(len(UserProfile.objects.all()),1)

#     def test_create_attendance(self):
#     	userProfile = UserProfile.objects.createUserProfile(self.tempProfile)
#     	attendance = Attendance.objects.createAttendance(userProfile,
#     															timezone.now())	
#     	att = Attendance.objects.getAttendanceByID(1)
#     	self.assertEqual(att.id,attendance)

#     def test_attendance_submit(self): 
#         userProfile = UserProfile.objects.createUserProfile(self.tempProfile)
#         attendance =  Attendance.objects.createAttendance(userProfile,
#         														timezone.now())
#         att = Attendance.objects.getAttendanceByID(attendance)
#         att_submit = AttendanceSubmit.objects.createAttendanceSubmit(att, userProfile)
#         self.assertNotEqual(att_submit, 0)
#         self.assertNotEqual(att_submit, None)
#         subList = AttendanceSubmit.objects.getSubmissionList(att)
#         self.assertEqual(len(subList),1)	
        													 

#     def test_model_can_create_a_bucketlist(self):
#         """Test the bucketlist model can create a bucketlist."""
        
# class ViewTestCase(TestCase):
#     """docstring for ClassName"""
#     def setUp(self):
#         #self.app_view = AppViews()
#         self.client = Client()        
#         self.URL = 'http://testserver/attendance_app/'
#         self.instructor_data = {'username' : 'username',
#                                 'chat_url' : 'url',
#                                 'first_name' : 'first',
#                                 'last_name' : 'last',
#                                 'email' : 'mail',
#                                 'role' : 'instructor'}
#         self.student_data = {'username' : 'student',
#                                 'chat_url' : 'student_url',
#                                 'first_name' : 'first',
#                                 'last_name' : 'last',
#                                 'email' : 'mail',
#                                 'role' : 'student'}                        

#     def test_create_form(self):
#         resp = self.client.post(self.URL, data = self.instructor_data)    
#         self.assertEqual(resp.status_code,200)
#         #self.assertEqual(resp.context, )
        
#     def test_submit_true(self):
#         resp = self.client.post(self.URL, data = self.instructor_data)  
#         resp1 = self.client.post(self.URL + 'submit', {'username' : 'username', 'chat_url' : 'url'})
#         self.assertEqual(resp1.status_code,200)
#         #print(resp1.content)

#     def test_submit_false(self):
#         resp1 = self.client.post(self.URL + 'submit', {'username' : 'u', 'chat_url' : 'u'})
#         #print(resp1.content)
#         self.assertEqual(resp1.status_code,200)
           

#     def test_submit_result_true(self):
#         resp = self.client.post(self.URL, data = self.instructor_data)  
#         resp_submit = self.client.post(self.URL + 'submit', {'username' : 'username', 'chat_url' : 'url'})
#         #print(resp_submit.content)
#         res_data = self.student_data.copy()
#         res_data['confirm_ans'] = 2
#         res_data['attendance_id'] = resp_submit.context.get('attendance_id')
#         resp_submit_result = self.client.post(self.URL + 'submitResult', res_data)
#         self.assertEqual(resp_submit_result.status_code, 200)     
#         #print(resp_submit_result.content)   

#     def test_submit_result_false(self):
#         resp = self.client.post(self.URL, data = self.instructor_data)  
#         resp_submit = self.client.post(self.URL + 'submit', {'username' : 'username', 'chat_url' : 'url'})
#         res_data = self.student_data.copy()
#         res_data['confirm_ans'] = 0
#         res_data['attendance_id'] = 0
#         resp_submit_result = self.client.post(self.URL + 'submitResult', res_data)
#         self.assertEqual(resp_submit_result.status_code, 200)  
#         #print(resp_submit_result.content)

#     def test_view(self):
#         resp = self.client.post(self.URL, data = self.instructor_data)  
#         resp_submit = self.client.post(self.URL + 'submit', {'username' : 'username', 'chat_url' : 'url'})
#         #print(resp_submit)      
#         res_view_no_submission = self.client.post(self.URL + 'view', {'attendance_id' : resp_submit.context.get('attendance_id')})
#         print(res_view_no_submission.content)      
#         self.assertEqual(res_view_no_submission.status_code, 200)
#         res_data = self.student_data.copy()
#         res_data['confirm_ans'] = 2
#         res_data['attendance_id'] = resp_submit.context.get('attendance_id')
#         resp_submit_result = self.client.post(self.URL + 'submitResult', res_data)
#         res_data1 = res_data.copy()
#         res_data1['username'] = 'student1'
#         resp_submit_result1 = self.client.post(self.URL + 'submitResult', res_data1)
#         res_view_some_submissions = self.client.post(self.URL + 'view', {'attendance_id' : resp_submit.context.get('attendance_id')})
#         self.assertEqual(res_view_some_submissions.status_code, 200)
#         print(res_view_some_submissions.content)       
#         res_view_wrong_id = self.client.post(self.URL + 'view', {'attendance_id' : 0})
#         self.assertEqual(res_view_wrong_id.status_code, 200)

class RocketSet:
    def __init__(self, url = None, auth_token = None, user_id = None):
        self.url = url
        self.auth_token = auth_token
        self.user_id = user_id


class TestRocketUsersAPI(TestCase):

    def setUp(self):
        rocket_setting = RocketSet()          
        self.rc_user_api = RocketUsersAPI(rocket_setting)


    def check_err_obj(self, err, res):
        self.assertNotEqual(err, None)
        self.assertNotEqual(err.get_code, None)
        self.assertNotEqual(err.get_msg, None)
        self.assertNotEqual(err.get_domain, None)
        print(err)
        self.assertEqual(res.is_success(), False)        


    def test_login_success(self):
        username = 'attendance'
        password = 'attendance'
        res_obj = self.rc_user_api.login(username, password)
        self.assertNotEqual(res_obj.get_uid(), None)
        self.assertNotEqual(res_obj.get_auth_token(), None)
        self.assertEqual(res_obj.is_success(), True)
        #print(r)
    
    def test_login_wrong_acc(self):
        res_obj = self.rc_user_api.login('username', 'password')
        err = res_obj.get_err()
        self.check_err_obj(err, res_obj)

    # def test_login_wrong_server(self):



    def test_get_users(self):
        res_obj = self.rc_user_api.get_users()
        self.assertEqual(res_obj.is_success(), True)
        self.assertEqual(len(res_obj.get_users()) > 0, True)
    #     #print(r)

    def test_get_users_faulty(self):
        print("====================")
        print("Test Get Users Faulty")
        print("====================")

        faulty_setting = RocketSet(auth_token='asdasd',user_id='wqeqwe')
        faulty_api = RocketUsersAPI(faulty_setting)
        res_obj = faulty_api.get_users()
        err = res_obj.get_err()
        self.check_err_obj(err, res_obj)

    def test_post_message(self):
        channel = 'general'
        text = 'hello world'
        r = self.rc_user_api.post_message(channel, text)
        self.assertNotEqual(r.get_msg, None)
        self.assertNotEqual(r.get_channel, "")
        #print(r.json().get('message'))

    #def test_post_message_wrong_acc(self):
