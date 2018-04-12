class RCLoginData:
	USERNAME = ''
	PASSWORD = ''

class RCLoginDataDefault(RCLoginData):
	USERNAME = 'attendance'
	PASSWORD = 'attendance'
		
#role constant admin, user
class RCRole:
	"""docstring for ClassName"""
	ADMIN = 'admin'
	USER = 'user'
	UNKNOWN = 'unknown'

#class ErrorMessage:

class RCActionLink:
	ACTION_PARAM = 'action_params'
	VALUE = 'value'
	ANSWER = 'answer'

class RCAPI:
	GET_USER = 'users.list'
	POST_MESSAGE = 'chat.postMessage'
	GET_USER_INFO = 'users.info'
	LOGIN = 'login'
	UPDATE_MESSAGE = 'chat.update'	

class Utility:
	@staticmethod
	def authenticate(self, params):
	    #params = request.GET
	    source = params.get('source')
	    username = RCLoginDataDefault.USERNAME
	    password = RCLoginDataDefault.PASSWORD
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
	                print(login_result.get_err())
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
	            print(login_result.get_err())
	            rocket_setting = None
	    return rocket_setting



