from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.http import JsonResponse

from attendance_app.models import Question, Answer, UserProfile, Attendance, AttendanceSubmit
from django.utils import timezone
question_key = 'Question'
#to be update using database
question = "What is 1 + 1"
answer = "2"

class AppViews:
	path = '/attendance_app'
	def __init__(self):
		self.question = "What is 1 + 1"
		self.answer = "2"		
		self.views = "views/"

	def userProfileFromRequest(self, requestParam):
		tempProfile = UserProfile() \
						.configID(requestParam.get('username'), requestParam.get('chat_url')) \
						.configName(requestParam.get('first_name'), requestParam.get('last_name'))\
						.configEmail(requestParam.get('email'), requestParam.get('role')) \
						.configCreatedOn(None)
		return tempProfile
	#@csrf_exempt	
	def createForm(self, request):
		#html = loader.get_template(self.views + "create.html")
		submitURL = request.scheme + "://" + request.get_host() + AppViews.path + '/submit' 
		#print(submitURL)

		requestParam = request.GET or request.POST
		#print(requestParam)
		user_prof = self.userProfileFromRequest(requestParam)
		instructor = UserProfile.objects.createUserProfile(self.userProfileFromRequest(requestParam))
		context = {"submitURL" : submitURL, 
					"username" : instructor.username, 
					"chat_url" : instructor.chat_url}
		response = HttpResponse(render(request, self.views + "create.html", context))
		#print(response.getvalue())
		return response
	# Create your views here.
	#@csrf_exempt
	def submit(self, request): 
		#print (request.get_full_path())
		submitResultURL = request.scheme  + "://" + request.get_host() + AppViews.path + '/submitResult'

		requestParam = request.GET or request.POST
		#print(requestParam)
		username = requestParam.get('username')
		chat_url = requestParam.get('chat_url')
		instructor = UserProfile.objects.hasUserWithRole(username, chat_url, 'instructor')
		if (instructor):
			attendanceID = Attendance.objects.createAttendance(instructor, timezone.now())
			context = {"question" : question, "submitResultURL" : submitResultURL, "attendance_id" : attendanceID}
			#html = loader.get_template(self.views + "question.html")		
			response = HttpResponse(render(request, self.views + "question.html", context))
			return response	
		else:	
			return HttpResponse('Only Registered instructors are allowed to use this feature.')

	#@csrf_exempt	
	def submitResult(self, request):
		#print (request.content_type)
		#print (request.POST)
		#print (request.GET)
		context = {}
		#html = loader.get_template(self.views + "confirm.html")
		requestParam = request.POST or request.GET
		#student = UserProfile.objects.createUserProfile(requestParam.get('username'), requestParam.get('chat_url'),
		#													requestParam.get('first_name'), requestParam.get('last_name'),
		#													requestParam.get('email'), timezone.now(), requestParam.get('role'))
		attendance = Attendance.objects.getAttendanceByID(requestParam.get('attendance_id'))
		if ((requestParam.get("confirm_ans") == self.answer) and 
			attendance):		
				context['confirmResult'] = "Success!"
				tempProfile = self.userProfileFromRequest(requestParam)
				submission = AttendanceSubmit.objects.createAttendanceSubmit(attendance  =attendance,  
																				tempProfile = self.userProfileFromRequest(requestParam))
		else:
			context['confirmResult'] = "Attendance check fail, please contact the instructor."	

		return HttpResponse(render(request, self.views + "confirm.html", context))	

	def view(self,request):
		requestParam = request.GET or request.POST
		context = {}
		attendance = Attendance.objects.getAttendanceByID(requestParam.get('attendance_id'))
		if (attendance):
			submissionList = AttendanceSubmit.objects.getSubmissionList(attendance)
			context['submission_list'] = submissionList
			print(submissionList)
			return HttpResponse(render(request, self.views + "view.html", context))
		else:
			return HttpResponse("No such attendance.")	
	def test_output(self,request):
		ob = test_class()
		return HttpResponse(ob.test_print())

	# print(response.getvalue())
	# return response	


# viewsets: create, edit, delete, post, get, list
#1. welcome user to create attendance
#2. create attendance
#3. allow student to check attendance
#4. list all attendances 
#5. list all checks of an attendance
#6. http://www.django-rest-framework.org/api-guide/views/

class APIViews:
	def __init__(self):
		self.data = ''

	@csrf_exempt	
	def createAttendance(self, request):
		view = AppViews()
		response = view.createForm(request)
		html_value = response.getvalue().decode("utf-8")

		return JsonResponse({
			"username": "Att",
			"icon_emoji": ":ghost:",
			"text": "Response text: " + 'create_attendance: ' + response.getvalue().decode("utf-8"),
			"attachments": [
				{
					"title": "Rocket.Chat",
					"title_link": "https://rocket.chat",
					"text": "Rocket.Chat, the best open source chat",
					"image_url": "https://rocket.chat/images/mockup.png",
					"color": "#764FA5"
				}, 
				{
					'key': 'create_attendance', 
					'html': response.getvalue().decode("utf-8") 				
				}
				]
			})

	@csrf_exempt
	def confirmCreateAttendance(self, request):
		# TODO: Need to create an attendance in database
		return JsonResponse({
				'key': 'confirm_create_attendance',
				'attendance_id': 'NULL'
			})

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

