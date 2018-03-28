import requests
from attendance_app.rc_return_obs import *
from attendance_app.rc_return_obs import RCErrDomain
# Instructions on using requests: http://docs.python-requests.org/en/latest/user/quickstart/
import json

class RocketSetting:
	API_PATH = "api/v1/"
	url = ""
	auth_token = ""
	user_id = ""

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
			msg = response.json().get('message') or response.json().get('error') or ""
			err.config_msg(requests.status_codes._codes[response.status_code][0] + msg)
			return err

	def get_users(self):
		headers = {'X-Auth-Token' : self.auth_token, 'X-User-Id' : self.user_id}
		getUsersUrl = self.url + "users.list"
		response = requests.get(getUsersUrl, headers=headers)
		r = response.json()
		obj = RCReturnObs(False)
		print("response.status_code: %s", response.status_code)

		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			users = r.get('users') 	    

			print("is_success: %s", is_success)			
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
			print(response.status_code)
			obj.config_err(err)			
		
		print("return obj: %s", obj)

		return obj

	def post_message(self, channel, text):
		headers = {'X-Auth-Token' : self.auth_token, 
					'X-User-Id' : self.user_id,
					'Content-type'	:	'application/json'}
		payload = {'channel' : channel, 'text' : text}
		payload = json.dumps(payload)
		post_message_url = self.url + 'chat.postMessage'
		response = requests.post(post_message_url, headers = headers, data = payload)
		print("payload: ",payload)
		r = response.json()
		print("response", r)
		obj = RCReturnObs(False)
		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			msg = r.get('message')			
			if (is_success and msg):
				obj = RCPostMessReturn(is_success)
				temp_mess = RCMessage(msg.get('_id'))
				temp_user = RCUserData(msg.get('u').get('_id'))
				temp_user.config_user(msg.get('u').get('name'),
									msg.get('u').get('username'))
				temp_mess.config(msg.get('msg'), temp_user).config_rid(msg.get('rid'))
				obj.config_msg(temp_mess).config_channel(r.get('channel'))
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
		get_url = self.url + 'users.info'
		response = requests.get(get_url, headers = headers, params = params)
		r = response.json()
		obj = RCReturnObs(False)
		if (RCErrDomain.is_rclogic_err(response.status_code)):
			is_success = r.get('success')
			user = r.get('user') 	    
			print("is_success: %s", is_success)			
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
			print(response.status_code)
			obj.config_err(err)			
		
		print("return obj: %s", obj)

		return obj		

		

	def login(self, username, password):
		payload = {'username' : username, 'password' : password}
		login_url = self.url + 'login'
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
    		
			
