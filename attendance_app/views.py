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
	def urlToConfirmCreateAttendance(self, request, path):
		params = request.GET
		source = params.get('source')
		submitURL = request.scheme + "://" + request.get_host() + AppViews.path \
			+ '/confirm_create_attendance?source=' + str(source)
		return submitURL

	def urlToConfirmSubmit(self, request, path):
		params = request.GET
		source = params.get('source')
		submitURL = request.scheme + "://" + request.get_host() + AppViews.path \
			+ '/confirm_submit?source=' + str(source)
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

	def createAttendanceObject(self, request):
		requestParam = request.GET or request.POST
		username = requestParam.get('username')
		chat_url = requestParam.get('chat_url')
		instructor = UserProfile.objects.hasUserWithRole(username, chat_url, 'instructor')
		if (instructor):
			attendanceID = Attendance.objects.createAttendance(instructor, timezone.now())
			return attendanceID
		else:	
			return None

	def contextForCreateAttendanceHTML(self, instructor, submitURL):
		context = {"submitURL" : submitURL, 
					"username" : instructor.username, 
					"chat_url" : instructor.chat_url}
		return context

	def contextForConfirmCreateAttendanceHTML(self, question, submitResultURL, attendance_id):
		context = {"question" : question, "submitResultURL" : submitResultURL, "attendance_id" : attendance_id}
		return context

class AppViews:
	path = '/attendance_app/html'
	def __init__(self):
		self.question = "What is 1 + 1"
		self.answer = "2"		
		self.viewPath = "views/"
		self.appControllers = AppControllers()

	#@csrf_exempt	
	def createAttendance(self, request):
		submitURL = self.appControllers.urlToConfirmCreateAttendance(request, AppViews.path)
		instructor = self.appControllers.createUserProfileIfNeeded(request)
		context = self.appControllers.contextForCreateAttendanceHTML(instructor, submitURL)
		response = HttpResponse(render(request, self.viewPath + "create.html", context))

		return response

	# Create your views here.
	#@csrf_exempt
	def confirmCreateAttendance(self, request): 
		submitResultURL = self.appControllers.urlToConfirmSubmit(request, AppViews.path)
		attendance_id = self.appControllers.createAttendanceObject(request)

		if (attendance_id):
			context = self.appControllers.contextForConfirmCreateAttendanceHTML(question, submitResultURL, attendance_id)
			response = HttpResponse(render(request, self.viewPath + "question.html", context))
			return response	
		else:	
			return HttpResponse('Only Registered instructors are allowed to use this feature.')

	#@csrf_exempt	
	def confirmSubmit(self, request):
		context = {}
		requestParam = request.POST or request.GET
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

