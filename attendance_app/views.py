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

class AppControllers:
	def submitUrlToConfirmForm(self, request, path):
		params = request.GET or request.POST
		source = params.get('source')
		submitURL = request.scheme + "://" + request.get_host() + AppViews.path \
			+ '/confirm_create_attendance?source=' + str(source)
		return submitURL

	def userProfileFromRequest(self, requestParam):
		tempProfile = UserProfile() \
						.configID(requestParam.get('username'), requestParam.get('chat_url')) \
						.configName(requestParam.get('first_name'), requestParam.get('last_name'))\
						.configEmail(requestParam.get('email'), requestParam.get('role')) \
						.configCreatedOn(None)
		return tempProfile

	def createUserProfileIfNeeded(self, request):
		requestParam = request.GET or request.POST
		#print(requestParam)
		user_prof = self.userProfileFromRequest(requestParam)
		instructor = UserProfile.objects.createUserProfile(user_prof)
		return instructor

	def contextForCreateHTML(self, instructor, submitURL):
		context = {"submitURL" : submitURL, 
					"username" : instructor.username, 
					"chat_url" : instructor.chat_url}
		return context

 
class AppViews:
	path = '/attendance_app/html/'
	def __init__(self):
		self.question = "What is 1 + 1"
		self.answer = "2"		
		self.viewPath = "views/"
		self.appControllers = AppControllers()

	#@csrf_exempt	
	def createAttendance(self, request):
		#html = loader.get_template(self.viewPath + "create.html")
		submitURL = self.appControllers.submitUrlToConfirmForm(request, AppViews.path)
		instructor = self.appControllers.createUserProfileIfNeeded(request)
		context = self.appControllers.contextForCreateHTML(instructor, submitURL)
		response = HttpResponse(render(request, self.viewPath + "create.html", context))

		return response

	# Create your views here.
	#@csrf_exempt
	def confirmCreateAttendance(self, request): 
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
			#html = loader.get_template(self.viewPath + "question.html")		
			response = HttpResponse(render(request, self.viewPath + "question.html", context))
			return response	
		else:	
			return HttpResponse('Only Registered instructors are allowed to use this feature.')

	#@csrf_exempt	
	def confirmSubmit(self, request):
		#print (request.content_type)
		#print (request.POST)
		#print (request.GET)
		context = {}
		#html = loader.get_template(self.viewPath + "confirm.html")
		requestParam = request.POST or request.GET
		#student = UserProfile.objects.createUserProfile(requestParam.get('username'), requestParam.get('chat_url'),
		#													requestParam.get('first_name'), requestParam.get('last_name'),
		#													requestParam.get('email'), timezone.now(), requestParam.get('role'))
		attendance = Attendance.objects.getAttendanceByID(requestParam.get('attendance_id'))
		if ((requestParam.get("confirm_ans") == self.answer) and 
			attendance):		
				context['confirmResult'] = "Success!"
				tempProfile = self.userProfileFromRequest(requestParam)
				submission = AttendanceSubmit.objects.createAttendanceSubmit(attendance = attendance,  
																				tempProfile = self.userProfileFromRequest(requestParam))
		else:
			context['confirmResult'] = "Attendance check fail, please contact the instructor."	

		return HttpResponse(render(request, self.viewPath + "confirm.html", context))	

	def viewAttendance(self,request):
		requestParam = request.GET or request.POST
		context = {}
		attendance = Attendance.objects.getAttendanceByID(requestParam.get('attendance_id'))
		if (attendance):
			submissionList = AttendanceSubmit.objects.getSubmissionList(attendance)
			context['submission_list'] = submissionList
			print(submissionList)
			return HttpResponse(render(request, self.viewPath + "view.html", context))
		else:
			return HttpResponse("No such attendance.")	
	def test_output(self,request):
		ob = test_class()
		return HttpResponse(ob.test_print())

	# print(response.getvalue())
	# return response	

