import requests
from Utility.rc_return_obs import *
from Utility.rc_return_obs import RCErrDomain
from Utility.default_data.rocket_data import RCAPI
# Instructions on using requests: http://docs.python-requests.org/en/latest/user/quickstart/
import json

class RocketSetting:
	API_PATH = "api/v1/"
	url = ""
	auth_token = ""
	user_id = ""

	def __str__(self):
		return "url: " + RocketSetting.url + '\n' +\
				"auth_token: " + RocketSetting.auth_token +\
				"user_id: " + RocketSetting.user_id

class RocketSettingKhang(RocketSetting):
	url = "http://localhost:3000/api/v1/"
	auth_token = ""
	user_id = ""

class RocketSettingTuyen(RocketSetting):
	url = "http://localhost:3000/api/v1/"
	auth_token = ""
	user_id = ""

	
class RocketSettingSandBox(RocketSetting):
	url = "http://52.14.66.21:3000/api/v1/"
	auth_token = '1adWh_2VA7EenY2_odNDukK5CyoFovJUNt0gpGrZheL'
	user_id = 'o7YSWHimW65oCGy5b'

class ActionLinkPrep:
	VID_CAM = 'icon-videocam'
	CALL_3RD = 'call_third_party_action'
	ICON = 'icon'
	LABEL = 'label'
	METHOD = 'method_id'
	PARAMS = 'params'

	def __init__(self, label, params):
		self.icon = ActionLinkPrep.VID_CAM
		self.label = label
		self.method_id = ActionLinkPrep.CALL_3RD
		self.params = params

	def buildActionLink(self):
		return {ActionLinkPrep.ICON: self.icon,
				ActionLinkPrep.LABEL: self.label,
				ActionLinkPrep.METHOD: self.method_id,
				ActionLinkPrep.PARAMS: self.params}

class ActionParameters:
	ACTION = 'action'
	METHOD = 'method'
	DELETE_AFTER_SUCCESS = 'delete_after_success'
	def __init__(self, action, method):
		self.action = action
		self.method = method	
		self.optional = {}
	def buildActionParameters(self):
		temp = {ActionParameters.ACTION: self.action,
				ActionParameters.METHOD: self.method}
		temp.update(self.optional)
		return temp		
				
	def config_optional(self, opt):
		self.optional.update(opt)
		return self			

class ActionLinkBuilder:
	ACTION_LINKS = 'actionLinks'
	ACTION_PARAM = 'actionParameters'
	def __init__(self, act_links, act_params):
		self.act_links = act_links
		self.act_params = act_params
	def buildObject(self):
		return {ActionLinkBuilder.ACTION_LINKS: self.act_links, 
				ActionLinkBuilder.ACTION_PARAM: self.act_params}
		 				

class RocketUsersAPI:

	def factory_setting(self):
		rocket_setting = RocketSettingSandBox()
		return rocket_setting

	def __init__(self, rocket_setting):
		self.default_setting = self.factory_setting()
		self.url = rocket_setting.url or self.default_setting.url
		self.auth_token = rocket_setting.auth_token or self.default_setting.auth_token
		self.user_id = rocket_setting.user_id or self.default_setting.user_id

	def config_err_obj(self, response):
			err = RCReturnObsErr()
			if (RCErrDomain.is_rcclient_err(response.status_code)):
				err.config_domain(RCErrDomain.CLIENT_DOMAIN) \
					.config_code(RCErrDomain.CLIENT_CODE)

			elif (RCErrDomain.is_rcserver_err(response.status_code)) :
				err = RCReturnObsErr().config_domain(RCErrDomain.SERVER_DOMAIN) \
											.config_code(RCErrDomain.SERVER_CODE)
			msg = response.json().get('m`essage') or response.json().get('error') or ""
			err.config_msg(requests.status_codes._codes[response.status_code][0] + msg)
			return err

	def get_users(self):
		headers = {'X-Auth-Token' : self.auth_token, 'X-User-Id' : self.user_id}
		getUsersUrl = self.url + RCAPI.GET_USER
		response = requests.get(getUsersUrl, headers=headers)
		r = response.json()
		obj = RCReturnObs(False)

		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			users = r.get('users') 	    

			if (is_success and users):	    
				obj = RCGetUserReturn(is_success, [])
				for json_obj in users:
					temp = RCUserData(json_obj.get('_id'))
					temp.config_user(json_obj.get('name'),
										json_obj.get('username')) \
						.config_roles(json_obj.get('roles'))
					obj.add_user(temp)
			else :
				err = RCReturnObsErr().config_domain(RCErrDomain.LOGIC_DOMAIN) \
										.config_code(RCErrDomain.LOGIC_CODE) \
										.config_msg(RCErrDomain.NULL_DATA)
				obj.config_err(err)				    
		else:
			err = self.config_err_obj(response)
			obj.config_err(err)			
		return obj

	def update_message(self, rid, mid, text):
		headers = {'X-Auth-Token' : self.auth_token, 
					'X-User-Id' : self.user_id,
					'Content-type'	:	'application/json'}	
		payload = json.dumps({'roomId': rid, 'msgId': mid, 'text': text})
		post_url = self.url + RCAPI.UPDATE_MESSAGE	
		response = requests.post(post_url, headers = headers, 
								data = payload)
		r = response.json()
		obj = RCReturnObs(False)
		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			msg = r.get('message')			
			if (is_success and msg):
				obj = RCUpdateMessReturn(is_success)
				temp_mess = RCMessage(msg.get('_id'))
				temp_user = RCUserData(msg.get('u').get('_id'))
				temp_user.config_user(msg.get('u').get('username'),
									msg.get('u').get('username'))
				temp_mess.config(msg.get('msg'), temp_user).config_rid(msg.get('rid'))
				obj.config_mess(temp_mess)
			else :
				err = RCReturnObsErr().config_domain(RCErrDomain.LOGIC_DOMAIN) \
										.config_code(RCErrDomain.LOGIC_CODE) \
										.config_msg(RCErrDomain.NULL_DATA)
				obj.config_err(err)					
		else:				
			err = self.config_err_obj(response)
			obj.config_err(err)
		return obj			

	def post_message(self, channel, text, opt=None):
		headers = {'X-Auth-Token' : self.auth_token, 
					'X-User-Id' : self.user_id,
					'Content-type'	:	'application/json'}			
		payload = {'channel' : channel, 'text' : text}
		if opt is not None:
			payload.update(opt) 	
		
		payload = json.dumps(payload)
		post_message_url = self.url + RCAPI.POST_MESSAGE
		response = requests.post(post_message_url, headers = headers, data = payload)
		r = response.json()
		obj = RCReturnObs(False)
		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			msgs = r.get('message')			
			if (is_success and msgs):
				obj = RCPostMessReturn(is_success)
				for msg in msgs:
					temp_mess = RCMessage(msg.get('_id'))
					temp_user = RCUserData(msg.get('u').get('_id'))
					temp_user.config_user(msg.get('u').get('name'),
										msg.get('u').get('username'))
					temp_mess.config(msg.get('msg'), temp_user).config_rid(msg.get('rid'))
					obj.add_msg(temp_mess)
				obj.config_channel(r.get('channel'))
			else :
				err = RCReturnObsErr().config_domain(RCErrDomain.LOGIC_DOMAIN) \
										.config_code(RCErrDomain.LOGIC_CODE) \
										.config_msg(RCErrDomain.NULL_DATA)
				obj.config_err(err)					
		else:				
			err = self.config_err_obj(response)
			obj.config_err(err)
		return obj	
	
	def get_user_by_username(self, username):
		headers = {'X-Auth-Token' : self.auth_token, 'X-User-Id' : self.user_id}
		params = {'username' : username}
		get_url = self.url + RCAPI.GET_USER_INFO
		response = requests.get(get_url, headers = headers, params = params)
		r = response.json()
		obj = RCReturnObs(False)
		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			user = r.get('user') 	    
			if (is_success and user):	    
				temp = RCUserData(user.get('_id'))
				temp.config_user(user.get('name'),
								user.get('username')) \
						.config_roles(user.get('roles'))
				obj = RCUserInfoReturn(is_success, temp)
			else :
				err = RCReturnObsErr().config_domain(RCErrDomain.LOGIC_DOMAIN) \
										.config_code(RCErrDomain.LOGIC_CODE) \
										.config_msg(RCErrDomain.NULL_DATA)
				obj.config_err(err)				    
		else:
			err = self.config_err_obj(response)
			obj.config_err(err)			
		return obj		

	def login(self, username, password):
		payload = {'username' : username, 'password' : password}
		login_url = self.url + RCAPI.LOGIN
		response = requests.post(login_url, json = payload)
		r = response.json()
		obj = RCReturnObs(False)
		if (RCErrDomain.is_rclogic_err(response.status_code)):
			data = r.get('data')
			is_success = r.get('status') == "success"
			if (is_success and data):
				obj = RCLoginReturn(is_success,
								data.get('userId'), data.get('authToken'))
			else:
				err = RCReturnObsErr().config_domain(RCErrDomain.LOGIC_DOMAIN) \
										.config_code(RCErrDomain.LOGIC_CODE) \
										.config_msg(r.get('error') or RCErrDomain.NULL_DATA)
				obj.config_err(err)								
		else:
			err = self.config_err_obj(response)
			obj.config_err(err)
		return obj	
    		
			
