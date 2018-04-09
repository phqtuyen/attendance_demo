# Main Controller of the backend
# determine application logic from each url
# Authors : Tuyen, Khang
# Last Date: 29/03/2018 

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CreateFormSerializer
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from .views import *
import htmlmin
from .networks import RocketSetting, RocketUsersAPI, ActionLinkPrep, ActionLinkBuilder, ActionParameters
from .default_data.rocket_data import RCLoginDataDefault
from attendance_app.models import RocketAPIAuthentication
# viewsets: create, edit, delete, post, get, list
#1. welcome user to create attendance
#2. create attendance
#3. allow student to check attendance
#4. list all attendances 
#5. list all checks of an attendance
#6. http://www.django-rest-framework.org/api-guide/views/

# API:
#  X-Auth-Token: pl59Z7F1S7c5MGIMi8ZtQ6d1XAtvafqwCoc1VFoyRCN
#  X-User-Id: KEPvCAsPtzniBTdYB
admin = 'admin'


class APIViews:
	path = '/attendance_app'
	confirm_create_attendance = '/confirm_create_attendance'
	def __init__(self):
		self.data = ''
		self.rocketPath = 'views/'
		self.appControllers = AppControllers()
		self.app_view = AppViews()

	def templateResponseDictionary(self, request):
		return {
			"username": "Attendance",
			"icon_emoji": ":ghost:",
			}
	def buildURL(self, request):
		return request.scheme + "://" + request.get_host() + APIViews.path 		
			
	def authenticate(self, params):
		#params = request.GET
		source = params.get('source')
		username = 'attendance'
		password = 'attendance'
		api_authentication = RocketAPIAuthentication.objects.getRocketAPIAuth(source)
		rocket_setting = RocketSetting()
		#print(source)
		rocket_setting.url = source + RocketSetting.API_PATH
		if (api_authentication):
			if api_authentication.rocket_chat_user_id != None:
				rocket_setting.user_id = api_authentication.rocket_chat_user_id

			if api_authentication.rocket_chat_auth_token != None:
				rocket_setting.auth_token = api_authentication.rocket_chat_auth_token        

			if rocket_setting.user_id == None or rocket_setting.auth_token == None:
				rocket_api = RocketUsersAPI(rocket_setting)
				login_result = rocket_api.login(username, password)
				if (login_result.is_sucess()):
					rocket_setting.user_id = login_result.get_uid()
					rocket_setting.auth_token = login_result.get_auth_token()
					api_authentication.set_user_id(login_result.get_uid()) \
										.set_auth_token(login_result.get_auth_token()) \
										.save()
				else :
						print(login_result.get_err())
						rocket_setting = None		
		else:				
				rocket_api = RocketUsersAPI(rocket_setting)
				login_result = rocket_api.login(username, password)
				if (login_result.is_success()):
					rocket_setting.user_id = login_result.get_uid()
					rocket_setting.auth_token = login_result.get_auth_token()
					RocketAPIAuthentication.objects.createRocketAPIAuth(source, login_result.get_uid(),
															login_result.get_auth_token())
				else :
						print(login_result.get_err())
						rocket_setting = None
		return rocket_setting			

	def format_html(self, response):
		html = response.getvalue().decode('utf-8')
		minified_html_value = htmlmin.minify(html, remove_empty_space = True)
		return minified_html_value	

	@csrf_exempt	
	def createAttendance(self, request):
		submitURL = self.appControllers.urlToConfirmCreateAttendance(request, AppViews.path)
		instructor = self.appControllers.createUserProfileIfNeeded(request)
		context = self.appControllers.contextForCreateAttendanceHTML(instructor, submitURL)

		print(request.GET.get('source'))
		res_html = self.format_html(self.app_view.createAttendance(request))
		rocket_setting = self.authenticate(request.GET)

		if (rocket_setting):
			rc_api = RocketUsersAPI(rocket_setting)
			response = rc_api.get_user_by_username(instructor.username)
			if (response.is_success()):
				#only pass param label
				{"actionLinks": [{"icon": "icon-videocam", 
								"label": "Submit", 
								"method_id": "call_third_party_action", 
								"params": "name=submit"},
								{"icon": "icon-videocam", 
								"label": "Cancel", 
								"method_id": "call_third_party_action", 
								"params": "name=cancel"}],
				"actionParameters": {"action": self.buildURL(request) + APIViews.confirm_create_attendance, 
  								"method": "get"}}
				submit_link = ActionLinkPrep('Submit', 'name=submit').buildActionLink()
				cancel_link = ActionLinkPrep('Cancel', 'name=cancel').buildActionLink()
				act_params = ActionParameters(self.buildURL(request) + APIViews.confirm_create_attendance, "post") \
												.buildActionParameters()
				act_link_obj = ActionLinkBuilder(act_links = [submit_link, cancel_link], 
													act_params = act_params).buildObject()				
				rc_api.post_message(response.user_data._id, res_html, act_link_obj)
			else:
				print('Fail to obtain user id.')
		return HttpResponse()		

	@csrf_exempt
	def confirmCreateAttendance(self, request):
		params = request.POST
		instructor_username = params.get('username')
		print(instructor_username)
		rocket_setting = self.authenticate(params)
		if (rocket_setting):
			rc_api = RocketUsersAPI(rocket_setting)
			response = rc_api.get_users()
			if (response.is_success()):
				users = response.get_users()
				users = list(filter(lambda user : user.name != None and user.username != None, users))
				res = self.app_view.confirmCreateAttendanceAPI(request)
				if (not res[0]):
					res_html = self.format_html(res[1])
					channels = map(lambda user : user._id, users)
					responses = map(lambda channel : rc_api.post_message(text = res_html, channel = channel), channels)
				else:	
					#print('came here')
					res_html_student = self.format_html(res[1])
					channels = list(map(lambda user : user._id, users))
					print("student channels ", channels)
					responses = rc_api.post_message(text = res_html_student, channel = channels)
					#print (responses)
					res_html_instructor = self.format_html(self.app_view.viewAttendance(request, {'attendance_id' : res[0]}))
					instructor_channel = next(filter(lambda user, instructor_username = instructor_username : user.username == instructor_username, users), '')
					#print("instructor channel" ,instructor_channel.username)
					response_instructor = rc_api.post_message(text = res_html_instructor, channel = instructor_channel._id)
			else:
				print('Fail to obtain user list.')	
		return HttpResponse()			

	@csrf_exempt
	def confirmSubmit(self, request):
		# TODO: Need to create an attendance submit in database
		params = request.POST
		res = self.app_view.confirmSubmit(request)
		res_html = self.format_html(res) 
		rocket_setting = self.authenticate(params)
		if (rocket_setting):
			rc_api = RocketUsersAPI(rocket_setting)
			response = rc_api.get_user_by_username(params.get('username'))
			if (response.is_success()):
				channel = response.user_data._id
				confirm_res = rc_api.post_message(channel = channel, text = res_html)
			else :
				print('Fail to get indvidual user info.')	
		return HttpResponse()

	@csrf_exempt
	def viewAttendance(self, request):
		params = request.POST
		res = self.app_view.viewAttendance(request)
		res_html = self.format_html(res)
		rocket_setting = self.authenticate(params)
		if (rocket_setting):
			rc_api = RocketUsersAPI(rocket_setting)
			response = rc_api.get_user_by_username(params.get('username'))
			if (response.is_success()):
				channel = response.user_data._id
				confirm_res = rc_api.post_message(channel = channel, text = res_html)
			else :
				print('Fail to get indvidual user info.')		
		return HttpResponse()