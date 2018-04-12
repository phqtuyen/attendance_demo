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
        print('userProfile: ', userProfile)
        if (not userProfile):
            userProfile = self.create(username=tempProfile.username,
                                         chat_url=tempProfile.chat_url)
            print('finish create before config from tempProfile')
            userProfile.configFromProfile(tempProfile)
            print('finish config from tempProfile')
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
        self.username = username or ""
        self.chat_url = chat_url or ""
        return self

    def configName(self, name):
        self.name = name or ""
        return self    
        
    def configEmail(self, email, role):
        self.email = email or ""
        self.role = role or ""
        return self

    def configCreatedOn(self, created_on):
        if (created_on):
            self.created_on = created_on
        else:
            self.created_on = timezone.now()
        return self    

    def configFromProfile(self, tempProfile):
        print('call config from profile.')
        self.name = tempProfile.name 
        print("tempProfile name while config:", tempProfile.name)
        self.email = tempProfile.email
        self.role = tempProfile.role
        self.created_on = tempProfile.created_on or timezone.now()
        self.save()
        return self

    def __str__(self):
        return self.username + ' ' + self.name + ' ' + self.email

class AttendanceManager(models.Manager):
    def createAttendance(self, created_by, created_on):
        attendance = self.create(created_by = created_by,
                                created_on = created_on)
        attendance.init_empty_fields()
        return attendance.id

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


class Attendance(models.Model):
    created_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
    created_on = models.DateTimeField(auto_now_add = True)
    messageid = models.CharField(max_length = 255)
    roomid    = models.CharField(max_length = 255)
    objects = AttendanceManager()    

    def init_empty_fields(self):
        self.messageid = ""
        self.roomid = ""
        self.save()
        return self
    # def config_message_id(self, mid):
    #     self.message_id = mid

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
            #print ('submissionList: ', submissionList)
            #print ('student username: ', submitted_by.id, 'attendance id: ', attendance.id)
            #print ('Data base: ', AttendanceSubmit.objects.all())
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
        
class AttendanceSubmit(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete = models.SET_NULL, null = True)
    submitted_on = models.DateTimeField(auto_now_add = True)	
    submitted_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
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


