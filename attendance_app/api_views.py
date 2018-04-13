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
from attendance_app.models import RocketAPIAuthentication, Attendance
import random
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
    confirm_submit = '/confirm_submit'
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
        source = params.get('source')
        username = 'attendance'
        password = 'attendance'
        api_authentication = RocketAPIAuthentication.objects.getRocketAPIAuth(source)
        rocket_setting = RocketSetting()
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
        res_html = self.format_html(self.app_view.createAttendance(request))
        rocket_setting = self.authenticate(request.GET)
        if (rocket_setting):
            rc_api = RocketUsersAPI(rocket_setting)
            response = rc_api.get_user_by_username(instructor.username)
            if (response.is_success()):
                submit_link = ActionLinkPrep('Confirm Create Attendance', 'name=submit').buildActionLink()
                act_params = ActionParameters(self.buildURL(request) + APIViews.confirm_create_attendance, "post")
                source = request.GET.get('source')
                act_params.config_optional({'source': source, 'username': instructor.username})
                act_params.config_optional({ActionParameters.DELETE_AFTER_SUCCESS: True})
                params = act_params.buildActionParameters()

                act_link_obj = ActionLinkBuilder(act_links = [submit_link],
                                                                                        act_params = params).buildObject()
                rc_api.post_message(response.user_data._id, res_html, act_link_obj)
            else:
                print('Fail to obtain user id.')
        return HttpResponse()

    @csrf_exempt
    def confirmCreateAttendance(self, request):
        params = request.POST
        instructor_username = params.get('username')
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
                    channels = list(map(lambda user : user._id, users))
                    responses = rc_api.post_message(text = res_html, channel = instructor_username)
                else:
                    res_html_student = self.format_html(res[1])
                    channels = [user._id for user in users if user.username != instructor_username]
                    random_answers = random.sample(range(1, 11), 5)
                    answer_links = []

                    for answer in random_answers:
                        answer_link = ActionLinkPrep('' + str(answer), 'value=' + str(answer)).buildActionLink()
                        answer_links.append(answer_link)

                    correct_answer_index = random.randint(0, 4)
                    correct_answer = random_answers[correct_answer_index]

                    act_params = ActionParameters(self.buildURL(request) + APIViews.confirm_submit, "post")
                    source = request.POST.get('source')
                    act_params = act_params.config_optional({'source': source,
                                                                                                    'username': instructor_username,
                                                                                                    'instructor_username': instructor_username,
                                                                                                    'answer': str(correct_answer),
                                                                                                    'attendance_id': res[0]})\
                                                                    .buildActionParameters()

                    act_link_obj = ActionLinkBuilder(act_links = answer_links,
                                                                                    act_params = act_params).buildObject()
                    responses = rc_api.post_message(text = res_html_student, channel = channels, opt = act_link_obj)

                    res_html_instructor = self.format_html(self.app_view.viewAttendance(request, {'attendance_id' : res[0], 'answer': str(correct_answer)})[1])
                    instructor_channel = [user._id for user in users if user.username == instructor_username]
                    response_instructor = rc_api.post_message(text = res_html_instructor, channel = instructor_channel)
                    if response_instructor.is_success():
                        Attendance.objects.set_message_id(res[0], response_instructor.msg[0]._id)\
                                                                .set_room_id(res[0], response_instructor.msg[0].rid)
                    else :
                        print('Fail to send message to instructor. Error message ', response_instructor.get_err())
            else:
                print('Fail to obtain user list.')
        return HttpResponse()

    @csrf_exempt
    def confirmSubmit(self, request):
        params = request.POST
        rocket_setting = self.authenticate(params)
        if (rocket_setting):
            rc_api = RocketUsersAPI(rocket_setting)
            res = self.app_view.confirmSubmitAPI(request)
            res_html = self.format_html(res[1])
            channel = params.get('channel')
            confirm_res = rc_api.post_message(channel = channel, text = res_html)
            if res[0] is True:
            	ins_res = self.app_view.viewAttendance(request)
            	ins_res_html = self.format_html(ins_res[1])
            	attendance = ins_res[0]
            	if attendance is not None:
            		rc_api.update_message(attendance.roomid, 
            								attendance.messageid,
            								ins_res_html)
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

