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
	CLIENT_SERVER = 'client_server'
	CLIENT_ONLY = 'client'
	SERVER_ONLY = 'server'




