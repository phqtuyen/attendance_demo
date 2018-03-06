from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

question_key = 'Question'
#to be update using database
question = "What is 1 + 1"
answer = "2"
@csrf_exempt
def index(request):
	if request.method == "GET" :
		print (request.GET)
		if question_key in request.GET:
			if request.GET.get(question_key) == answer:
				html = loader.get_template("views/confirm.html")
				response = HttpResponse(html.render())
			else: 
				context = {"question" : question}
				html = loader.get_template("views/question.html")		
				response = HttpResponse(html.render(context=context))
					
		else:	
			html = loader.get_template("views/create.html")
			print (type(str(html.render())) )
			response = HttpResponse(html.render() % {'question': question})
	elif request.method == "POST" :
		context = {"question" : question}
		html = loader.get_template("views/question.html")		
		response = HttpResponse(html.render(context=context))
	print(response.getvalue())
	return response	
# Create your views here.
