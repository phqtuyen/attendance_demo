from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseServerError
from django.template import loader, RequestContext
#from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.http import JsonResponse
from Utility.views import AbstractControllers
from Utility.networks import ActionLinkPrep, ActionLinkBuilder, ActionParameters
from Utility.default_data.rocket_data import *
from feedback.models import FeedbackSession, StudentFeedback
from django.utils import timezone
from urllib.parse import parse_qs
from feedback.models import StudentFeedbackManager
# Create your views here.

class ActionLinkView:
    HAPPY = 'HAPPY'
    NEUTRAL = 'NEUTRAL'
    SAD = 'SAD'

    def prepare_choice(self, choice):
        return ActionLinkPrep(choice, 'value=' + choice).buildActionLink()

    def prepare_action_links(self):
        answer_links = [self.prepare_choice(ActionLinkView.HAPPY),
                                        self.prepare_choice(ActionLinkView.NEUTRAL),
                                        self.prepare_choice(ActionLinkView.SAD)]

        return answer_links

    def wrap_act_params(self, params):
        return {'source': params.get('source'),
                        'username': '',
                        'admin_username': params.get('username'),
                        'feedback_id': params.get('feedback_id')}

    def prepare_action_params(self, params):
        act_params = ActionParameters(params.get('url'), params.get('method'))
        act_params.config_optional(self.wrap_act_params(params))
        return act_params.buildActionParameters()

    def prepare_act_link_obj(self, params):
        act_links = self.prepare_action_links()
        act_params = self.prepare_action_params(params)
        return ActionLinkBuilder(act_links = act_links,
                                                        act_params = act_params).buildObject()

class AppController(AbstractControllers):
    CHOICE_MAP = {ActionLinkView.HAPPY : 2,
                            ActionLinkView.SAD : 0,
                            ActionLinkView.NEUTRAL: 1}

    def __init__(self):
        AbstractControllers.__init__(self)

    def create_feedback_session(self, params):
        admin = self.isAdmin(params)
        print ('this is admin: ', admin)
        if admin:
            feedback_id = FeedbackSession.objects.createAttendance(admin,
                                                                                                                    timezone.now())
            print ('Create feedback_id successfully: ', feedback_id)
            return feedback_id
        else:
            return None

    def url_to_confirm_submit(self, request):
        return request.scheme + "://" + request.get_host() + "/" + 'feedback_app/' + 'confirm_submit'

    def aggregate_feedback(self, session_id):
        choice_stat = {}
        choice_stat.update({'total':
                                                StudentFeedback.objects.calc_total(session_id)})
        for choice, value in AppController.CHOICE_MAP.items():
            num = StudentFeedback.objects.calc_num_choice(value, session_id)
            choice_stat.update({choice: num})
        return choice_stat

    def get_choice(self, params):
        query_str = params.get(RCActionLink.ACTION_PARAM)
        if query_str is not None:
            answer_dict = parse_qs(query_str)
            return answer_dict.get(RCActionLink.VALUE)[0]
        else:
            return None

class GeneralView:
    path = 'feedback/html'

    def __init__(self):
        self.view_path = "feedback_views/"
        self.app_controller = AppController()
        self.create_feedback_path = 'create_feedback'
        self.confirm_create_feedback_path = 'confirm_create_feedback'
        self.confirm_submit_path = 'confirm_submit'
        self.view_feedback_path = 'view_feedback'

    #first call from RC is always GET, I dont know why people want it to be GET
    #ple
    def confirm_create_feedback(self, request):
        params = request.GET
        admin = self.app_controller.createUserProfileIfNeeded(params)
        feedback_id = self.app_controller.create_feedback_session(params)
        context = {}
        question = params.get('question')
        if question:
            context.update({'has_question': True, 'question': question})
        if (feedback_id):
            return (feedback_id, render(request, self.view_path + "question.html", context))
        else:
            return (None ,HttpResponse('Fail to create feedback session.'))

    def further_comment(self, request):
        params = request.GET
        choice = self.app_controller.get_choice(params)
        context = {'choice': choice or ''}
        context.update({'username': params.get('username') or ''})
        context.update({'feedback_id': params.get('feedback_id') or ''})
        context.update({'confirm_submit_url': self.app_controller.url_to_confirm_submit(request)})
        return render(request, self.view_path + 'further_comment.html', context)


    def view_feedback(self, request, params = {}):
        #params = dict(request.POST).copy().update(params)
        context = {}
        session_id = params.get('feedback_id')
        methods_list = [method_name for method_name in dir(StudentFeedback.objects)
                        if callable(getattr(StudentFeedback.objects, method_name))]
        method_list_2 =  [method_name for method_name in dir(FeedbackSession.objects)
                    if callable(getattr(FeedbackSession.objects, method_name))]           
        print('method list StudentFeedback: ', methods_list)
        print('method list FeedbackSession: ', method_list_2)
        #print('method list ob: ', method_list_3)
        if session_id:
            if FeedbackSession.objects.has_session_with_id(FeedbackSession, session_id)\
                and StudentFeedback.objects.has_submissions(session_id):
                context.update({'has_submissions': True})
                choice_stat = self.app_controller.aggregate_feedback(session_id)
                context.update({'choice_stat': choice_stat})
            else:
                context['has_submissions'] = False
            return (session_id, render(request, self.view_path + 'view.html', context))
        else:
            print('Invalid feedback session id.')

    def confirm_submit(self, request):
    	print("params to confirm submit: ", params)
    	feedback_session = FeedbackSession.objects.get_session_by_id(params.get('feedback_id'))
    	user_profile = self.app_controller.createUserProfileIfNeeded(params)
    	submitted = StudentFeedback.student_submitted(submitted_by = user_profile,
    													feedback_session = feedback_session)
    	if not submitted:
    		submission = StudentFeedback.objects.create_student_feedback(feedback_session,
    																	user_profile)
    		return (True, HttpResponse('Submission success.'))
    	else:
    		return (False, HttpResponse('You can only make submission once.'))	
