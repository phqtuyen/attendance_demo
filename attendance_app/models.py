from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
# Create your models here.

#Manager Class for UserProfile         

class UserProfileManager(models.Manager):
    #create new userprofile if not existed 
    def createUserProfile(self, tempProfile):
        userProfile = UserProfile.objects.hasUserProfile(username=tempProfile.username, 
                                                            chat_url=tempProfile.chat_url)
        if (not userProfile):
            userProfile = self.create(username=tempProfile.username,
                                         chat_url=tempProfile.chat_url)
            userProfile.configFromProfile(tempProfile)
            userProfile.save()
        return userProfile    

    
    def hasUserProfile(self, username, chat_url):
        try:
            userProfile = UserProfile.objects.get(username__iexact = username, chat_url__iexact = chat_url)
            return userProfile
        except MultipleObjectsReturned:
            print ("More than one user with the same username and chat_url.")
            return None
        except ObjectDoesNotExist:
            print ("UserProfile does not exist.")
            return None

    def hasUserWithRole(self, username, chat_url, role):
        user = self.hasUserProfile(username, chat_url)
        if (user):
            if (user.role == role):
                return user
            else:
                return None
        return user            

class UserProfile(models.Model):
    username = models.CharField(max_length = 150)
    chat_url = models.CharField(max_length = 255)
    name = models.CharField(max_length = 150)
    email = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    role = models.CharField(max_length = 40)
    objects = UserProfileManager()

    def configID(self, username, chat_url):
        self.username = (username or "").strip()
        self.chat_url = (chat_url or "").strip()
        return self

    def configName(self, name):
        self.name = (name or "").strip()
        return self    
        
    def configEmail(self, email, role):
        self.email = (email or "").strip()
        self.role = (role or "").strip()
        return self

    def configCreatedOn(self, created_on):
        if (created_on):
            self.created_on = created_on
        else:
            self.created_on = timezone.now()
        return self    

    def configFromProfile(self, tempProfile):
        self.name = tempProfile.name 
        self.email = tempProfile.email
        self.role = tempProfile.role
        self.created_on = tempProfile.created_on or timezone.now()
        self.save()
        return self

    def __str__(self):
        return self.username + ' ' + self.name + ' ' + self.email + ' ' + self.role

class QuizSessionManager(models.Manager):

    class Meta:
        abstract = True

    def createAttendance(self, created_by, created_on):
        attendance = self.create(created_by = created_by,
                                created_on = created_on)
        attendance.init_empty_fields()
        return attendance.id

    def create_quiz_session(self, created_by, created_on, source):
        quiz_session = self.create(created_by = created_by,
                                    created_on = created_on,
                                    source = source)
        quiz_session.init_empty_fields()
        return quiz_session.id

    def has_session_with_id(self, table_class, session_id):
        result = table_class.objects.filter(id__exact = session_id)
        return len(result) > 0

    def get_session_by_id(self, table_class, session_id):
        try:
            session = table_class.objects.get(id__exact = session_id)
            return session
        except MultipleObjectsReturned:
            print ("More than one objects with the same id.")
            return None
        except ObjectDoesNotExist:
            print ("Object with this id does not exist.")
            return None

    # def set_session_message_id(self, table_class, session_id, message_id):
    #     session = self.get_session_by_id(table_class, session_id)

    def set_message_id(self, attendance_id, message_id):   
        attendance = self.getAttendanceByID(attendance_id)
        if (attendance != None):
            attendance.messageid = message_id
            attendance.save()
        return self       

    def set_room_id(self, attendance_id, room_id):   
        attendance = self.getAttendanceByID(attendance_id)
        if (attendance != None):
            attendance.roomid = room_id
            attendance.save()
        return self                                

    def getAttendanceByID(self, attendanceID):
        try:
            attendance = Attendance.objects.get(id__exact = attendanceID)
            return attendance
        except MultipleObjectsReturned:
            print ("More than one objects with the same username and chat_url.")
            return None
        except ObjectDoesNotExist:
            print ("Object does not exist.")
            return None   

    def get_session_by_id(self, session_id):
        try:
            session = self.get(id__exact = session_id)
            return session
        except MultipleObjectsReturned:
            print ("More than one objects with the same id.")
            return None
        except ObjectDoesNotExist:
            print ("Object does not exist.")
            return None            

class AttendanceManager(QuizSessionManager):

    class Meta:
        abstract = True

#base class for any quiz session
class QuizSession(models.Model):
    created_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
    created_on = models.DateTimeField(auto_now_add = True)
    source = models.CharField(max_length = 255, default = '')
    messageid = models.CharField(max_length = 255)
    roomid    = models.CharField(max_length = 255)

    class Meta:
        abstract = True    

    def init_empty_fields(self):
        self.messageid = ""
        self.roomid = ""
        # self.source = ""
        self.save()
        return self

    def set_room_id(self, room_id):
        self.roomid = room_id
        self.save()
        return self

    def set_source(self, source):
        self.source = source
        self.save()
        return self
        
    def set_message_id(self, message_id):
        self.messageid = message_id
        self.save()
        return self

class Attendance(QuizSession):

    objects = AttendanceManager()    


class StudentSubmissionManager(models.Manager):
    class Meta:
        abstract = True



class AttendanceSubmitManager(models.Manager):
    def createAttendanceSubmit(self, attendance, tempProfile):

        submitted_by = UserProfile.objects.createUserProfile(tempProfile) 
        submitted_by_list = self.student_submitted(submitted_by, attendance)
        if (not submitted_by_list):
            attendanceSubmit = self.create(attendance = attendance, 
                                            submitted_on = timezone.now(), 
                                            submitted_by = submitted_by,
                                            correct_submission = False)
            attendanceSubmit.save()
            return attendanceSubmit.id

        return submitted_by_list[0].id               
        
    def createAttSubmit(self, attendance, submitted_on, submitted_by):
        submission = self.create(attendance = attendance, 
                                    submitted_on = submitted_on, 
                                    submitted_by = submitted_by)   
        attendanceSubmit.save()
        return submission.id

    def verify_submission(self, submitted_by, attendance):
        try:
            submission = self.get(submitted_by__id__exact = submitted_by.id,
                                    attendance__id__exact = attendance.id)
            submission.correct_submission = True
            submission.save()
        except Exception:
            print (Exception)
            return None
        return self        

    def student_submitted(self, submitted_by, attendance):
        try :
            submissionList = self.filter(submitted_by__id__exact = submitted_by.id,
                                            attendance__id__exact = attendance.id)
            if (not submissionList):
                return None
            else:
                return submissionList    
        except Exception:
            print (Exception)    
            return None        

    def getSubmissionList(self, attendance):
        try :
            submissionList = self.filter(attendance__id__exact = attendance.id)
            if (not submissionList):
                return None
            else:
                return submissionList    
        except Exception:
            print (Exception)    
            return None

class StudentSubmission(models.Model):
    submitted_on = models.DateTimeField(auto_now_add = True)    
    submitted_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)

    class Meta:
        abstract = True
       
class AttendanceSubmit(StudentSubmission):
    attendance = models.ForeignKey(Attendance, on_delete = models.SET_NULL, null = True)
    correct_submission = models.BooleanField()
    objects = AttendanceSubmitManager()

    def format_str(self, att_id, username, correct, name, email):
        return 'att_id: ' + str(att_id)\
                 + ' stud_id: ' + str(username)\
                 + ' correct: ' + str(correct)\
                 + ' name: ' + str(name)\
                 + ' email: ' + str(email)

    def __str__(self):
        return self.format_str(self.attendance.id, self.submitted_by.id,
                                 self.correct_submission, self.submitted_by.name, 
                                 self.submitted_by.email)

class RocketAPIAuthenticationManager(models.Manager):
    def createRocketAPIAuth(self, url, user_id, auth_token):
        api_authentication = self.create(rocket_chat_url = url, 
                                    rocket_chat_user_id = user_id, 
                                    rocket_chat_auth_token = auth_token)   
        api_authentication.save()
        return api_authentication.id


    def getRocketAPIAuth(self, url):
        try:
            api_authentication = RocketAPIAuthentication.objects.get(rocket_chat_url__exact = url)
            return api_authentication
        except MultipleObjectsReturned:
            print ("More than one objects with the same username and chat_url.")
            return None
        except ObjectDoesNotExist:
            print ("Object does not exist.")
            return None               

class RocketAPIAuthentication(models.Model):
    rocket_chat_user_id = models.CharField(max_length = 100)
    rocket_chat_auth_token = models.CharField(max_length = 150)
    rocket_chat_url = models.CharField(max_length = 255)

    objects = RocketAPIAuthenticationManager()

    def get_user_id(self):
        return self.rocket_chat_user_id

    def get_auth_token(self):
        return self.rocket_chat_auth_token

    def get_url(self):
        return self.rocket_chat_url

    def set_user_id(self, uid):
        self.rocket_chat_user_id = uid
        #self.save()
        return self

    def set_auth_token(self, token):
        self.rocket_chat_auth_token = token
        #self.save()
        return self

    def set_url(self, url):
        self.rocket_chat_url = url
        #self.save()
        return self


