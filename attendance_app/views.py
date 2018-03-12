from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt
from .test import test_class
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CreateFormSerializer
from django.contrib.auth.models import User, Group

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
	#@csrf_exempt	
	def createForm(self,request):
		html = loader.get_template(self.views + "create.html")
		submitURL = request.scheme + "://" + request.get_host() + AppViews.path + '/submit' 
		print(submitURL)
		context = {"submitURL" : submitURL}
		response = HttpResponse(html.render(context))
		print(response.getvalue())
		return render(request, self.views + "create.html", context)
	# Create your views here.
	#@csrf_exempt
	def submit(self,request): 
		print (request.get_full_path())
		submitResultURL = request.scheme  + "://" + request.get_host() + AppViews.path + '/submitResult'
		context = {"question" : question, "submitResultURL" : submitResultURL}
		html = loader.get_template(self.views + "question.html")		
		response = HttpResponse(html.render(context=context))
		return render(request, self.views + "question.html", context)

	#@csrf_exempt	
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
		return render(request, self.views + "confirm.html", context)	
		
	def view(self,request):
		return

	def test_output(self,request):
		ob = test_class()
		return HttpResponse(ob.test_print())

	print(response.getvalue())
	return response	
	
class CreateForm(viewsets.ModelViewSet):
    queryset = User.objects.all()[:1]
    serializer_class = CreateFormSerializer

class ConfirmForm(viewsets.ModelViewSet):
	queryset = User.objects.all()[:1]
	serializer_class = ConfirmFormSerializer	


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
