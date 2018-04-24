from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from user.models import UserProfile
# Create your models here.

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
        # print ('attendance to be update', attendance)
        if (attendance != None):
            attendance.messageid = message_id
            attendance.save()
        return self       

    def set_room_id(self, attendance_id, room_id):   
        attendance = self.getAttendanceByID(attendance_id)
        # print('attendance to be update: ', attendance)
        if (attendance != None):
            attendance.roomid = room_id
            attendance.save()
        return self                                

    def getAttendanceByID(self, attendanceID):
        try:
            attendance = self.get(id__exact = attendanceID)
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

    def __str__(self):
        return 'id: ' + str(self.id)\
                + ' created_by: ' + self.created_by.username\
                + ' source: ' + self.source\
                + ' messageid: ' + self.messageid\
                + ' roomid: ' + self.roomid + str("\n")

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

