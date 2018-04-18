from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader, RequestContext
from .serializers import UserSerializer, GroupSerializer, CreateFormSerializer
from django.contrib.auth.models import User, Group
from .views import *
from Utility.rc_api_interaction import APIFunctions
from Utility.networks import RocketUsersAPI, ActionLinkPrep, ActionLinkBuilder, ActionParameters
from Utility.views import AppController, GeneralView, ActionLinkView
import htmlmin

class FeedbackAPIView(APIFunctions):
	path = '/feedback_app'
	confirm_create_feedback = '/confirm_create_feedback'
	confirm_submit = '/confirm_submit'
	FURTHER_COMMENT = '/further_commnet'

	def __init__(self):
		APIFunctions.__init__(path)
		self.app_controller = AppController()
		self.app_view = GeneralView()
		self.act_link_view = ActionLinkView()

	def confirm_create_feedback(self, request):
		params = request.POST
		admin_username = params.get('username')
		rocket_setting = self.authenticate(params)
		if rocket_setting:
			rc_api = RocketUsersAPI(rocket_setting)
			response = rc_api.get_users()
			if response.is_success():
				all_acc = response.get_users()
				users = self.get_users(all_acc, admin_username)
				admin = self.get_admin(all_acc, admin_username)
				to_user_response = self.app_view.confirm_create_feedback(request)
				if to_user_response[0]:
					feedback_id = to_user_response[0]
					to_user_html = self.format_html(to_user_response[1])
					temp_params = params.copy()
					temp_params.update({'admin_username': admin_username})
					temp_params.update({'feedback_id': feedback_id, 'method': 'post'})
					temp_params.update({'url': self.build_URL(request) 
												+ FeedbackAPIView.FURTHER_COMMENT})
					act_link_obj = self.act_link_view.prepare_act_link_obj(temp_params)
					to_user_api_res = rc_api.post_message(text = to_user_html,
															channel = users,
															opt = act_link_obj)
					to_admin_respose = self.app_view.view_feedback(request, {'feedback_id': feedback_id})
					to_admin_html = self.format_html(to_admin_respose[1])
					to_admin_api_res = rc_api.post_message(text = to_admin_html,
															channel = admin)

			else:
				print ('Fail to obtain user')

	def function(self):
						pass				


