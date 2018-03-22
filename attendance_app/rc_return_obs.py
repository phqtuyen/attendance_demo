class RCUserData:
	def __init__(self, _id):
		self._id = _id
		self.name = ""
		self.username = ""

	def config_user(self, name, username):
		self.name = name
		self.username = username	

class RCMessage:
	def __init__(self, _id):
		self._id = _id
		self.msg = ""
		self.sender = None
		self.rid = ""

	def config(self, msg, rc_user):
		self.msg = msg
		self.sender = rc_user
		return self

	def config_rid(self, rid):
		self.rid = rid
		return self

class RCErrDomain:
	RCLogicErr = [200, 201, 202, 203, 204, 205, 206, 207, 208, 226]
	RCClientErr = [400, 401, 402, 403, 404, 405, 406, 407, 409, 410,
					 411, 412, 413, 414, 415, 416, 417, 418, 421, 422]
	RCServerErr = range(500,512)
	
	LOGIC_DOMAIN = 'RC_LOGIC_ERROR'
	CLIENT_DOMAIN = 'RC_DOMAIN_ERROR'
	SERVER_DOMAIN = 'RC_SERVER_ERROR'

	LOGIC_CODE = 200
	CLIENT_CODE = 400
	SERVER_CODE = 500
	
	NULL_DATA = 'NULL_DATA'	

	@staticmethod
	def is_rclogic_err(code):
		return code in RCErrDomain.RCLogicErr

	@staticmethod	
	def is_rcclient_err(code):
		return code in RCErrDomain.RCClientErr

	@staticmethod	
	def is_rcserver_err(code):
		return code in RCErrDomain.RCServerErr




class RCReturnObsErr:
	def config_code(self, code):
		self.code = code
		return self

	def config_domain(self, domain):
		self.domain = domain
		return self

	def config_msg(self, msg):
		self.msg = msg
		return self

	def get_code(self):
		return self.code

	def get_msg(self):
		return self.msg

	def get_domain(self):
		return self.domain

	def __str__(self):
		return ' '.join([self.domain, str(self.code), self.msg])		

class RCReturnObs:
	def __init__(self, success):
		self.success = success
		self.err = None

	def config_err(self, err):
		self.err = err
		return self

	def get_err(self):
		return self.err	

	def is_success(self):
		return self.success

class RCGetUserReturn(RCReturnObs):
	def __init__(self, success, users):
		RCReturnObs.__init__(self, success)
		self.users = users

	def add_user(self, user):
		self.users.append(user)

	def get_users(self):
		return self.users

class RCLoginReturn(RCReturnObs):
	def __init__(self, success, uid, auth_token):
		RCReturnObs.__init__(self, success)
		self.uid = uid
		self.auth_token = auth_token

	def get_uid(self):
		return self.uid

	def get_auth_token(self):
		return self.auth_token

class RCPostMessReturn(RCReturnObs):
	def __init__(self, success):
		RCReturnObs.__init__(self, success)
		self.msg = None
		self.channel = ""

	def config_msg(self, msg):
		self.msg = msg
		return self

	def config_channel(self, channel):
		self.channel = channel
		return self

	def get_msg(self):
		return self.msg

	def get_channel(self):
		return self.channel


						