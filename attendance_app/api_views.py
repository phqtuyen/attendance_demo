from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CreateFormSerializer
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from .views import *
import htmlmin


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


class APIViews:
	path = '/attendance_app'

	def __init__(self):
		self.data = ''
		self.rocketPath = 'views/'
		self.appControllers = AppControllers()

	def templateResponseDictionary(self, request):
		return {
			"username": "Attendance",
			"icon_emoji": ":ghost:",
			}

	@csrf_exempt	
	def createAttendance(self, request):
		submitURL = self.appControllers.urlToConfirmCreateAttendance(request, AppViews.path)
		instructor = self.appControllers.createUserProfileIfNeeded(request)
		context = self.appControllers.contextForCreateAttendanceHTML(instructor, submitURL)

		response = HttpResponse(render(request, self.rocketPath + "create.html", context))

		html_value = response.getvalue().decode("utf-8")
		minified_html_value = htmlmin.minify(html_value, remove_empty_space=True)
		templateDictionary = self.templateResponseDictionary(request)
		templateDictionary['text'] = minified_html_value
		
		return JsonResponse(templateDictionary)

	@csrf_exempt
	def confirmCreateAttendance(self, request):
		# TODO: Need to create an attendance in database
		# TODO: How to deal with username + password from rocket.chat
		username = 'attendance'
		password = 'attendance'

		print ("confirmCreateAttendance")

		submitResultURL = self.appControllers.urlToConfirmSubmit(request, AppViews.path)
		attendance_id = self.appControllers.createAttendanceObject(request)
		templateDictionary = self.templateResponseDictionary(request)

		if (attendance_id):
			context = self.appControllers.contextForConfirmCreateAttendanceHTML(question, submitResultURL, attendance_id)
		else:	
			templateDictionary['text'] = 'Your attendance check has been sent to every student, source = ' \
				+ source

		return JsonResponse(templateDictionary)

	@csrf_exempt
	def confirmSubmit(self, request):
		# TODO: Need to create an attendance submit in database

		view = AppViews()
		response = view.submitResult(request)
		html_value = response.getvalue().decode("utf-8")

		return JsonResponse({
				'key': 'confirm_submit',
				'html': html_value
			})	

	@csrf_exempt
	def viewAttendance(self, request):
		view = AppViews()
		response = view.view(request)
		html_value = response.getvalue().decode("utf-8")

		return JsonResponse({
				'key': 'view_attendance',
				'html': html_value
			})	
