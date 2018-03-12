from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .test import test_class
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
	@csrf_exempt	
	def createForm(self,request):
		html = loader.get_template(self.views + "create.html")
		submitURL = request.scheme + "://" + request.get_host() + AppViews.path + '/submit' 
		print(submitURL)
		context = {"submitURL" : submitURL}
		response = HttpResponse(html.render(context=context))
		print(response.getvalue())
		return response	
	# Create your views here.
	@csrf_exempt
	def submit(self,request): 
		print (request.get_full_path())
		submitResultURL = request.scheme  + "://" + request.get_host() + AppViews.path + '/submitResult'
		context = {"question" : question, "submitResultURL" : submitResultURL}
		html = loader.get_template(self.views + "question.html")		
		response = HttpResponse(html.render(context=context))
		return response	

	@csrf_exempt	
	def submitResult(self, request):
		print (request.content_type)
		print (request.POST)
		print (request.GET)
		context = {}
		html = loader.get_template(self.views + "confirm.html")
		if (request.POST.get("confirm_ans") == self.answer):
			context['confirmResult'] = "Success!"
		else:
			context['confirmResult'] = "Attendance check fail, please contact the instructor."	
		return HttpResponse(html.render(context=context))	
		
	def view(self,request):
		return

	def test_output(self,request):
		ob = test_class()
		return HttpResponse(ob.test_print())