import requests
from attendance_app.rc_return_obs import *
# Instructions on using requests: http://docs.python-requests.org/en/latest/user/quickstart/

class RocketSetting:
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

	def get_users(self):
	    headers = {'X-Auth-Token' : self.auth_token, 'X-User-Id' : self.user_id}
	    getUsersUrl = self.url + "users.list"
	    r = requests.get(getUsersUrl, headers=headers).json()
	    obj = RCGetUserReturn(r.get('success'), [])
	    for json_obj in r.get('users'):
	    	temp = RCUserData(json_obj.get('_id'))
	    	temp.config_user(json_obj.get('name'),
	    						json_obj.get('username'))
	    	obj.add_user(temp)

	    return obj

	def post_message(self, channel, text):
		headers = {'X-Auth-Token' : self.auth_token, 
					'X-User-Id' : self.user_id,
					'Content-type'	:	'application/json'}
		payload = {'channel' : channel, 'text' : text}
		post_message_url = self.url + 'chat.postMessage'
		r = requests.post(post_message_url, headers = headers, json = payload).json()
		obj = RCPostMessReturn(r.get('success'))
		msg = r.get('message')
		if (msg):
			temp_mess = RCMessage(msg.get('_id'))
			temp_user = RCUserData(msg.get('u').get('_id'))
			temp_user.config_user(msg.get('u').get('name'),
									msg.get('u').get('username'))
			temp_mess.config(msg.get('msg'), temp_user).config_rid(msg.get('rid'))
			obj.config_msg(temp_mess).config_channel(r.get('channel'))
			return obj

		return None	

	def login(self, username, password):
		payload = {'username' : username, 'password' : password}
		login_url = self.url + 'login'
		r = requests.post(login_url, json = payload).json()
		data = r.get('data')
		if (data):
			obj = RCLoginReturn(r.get('status') == 'success',
								data.get('userId'), data.get('authToken'))
			return obj
    				
		return None	
