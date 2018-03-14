from django.db import models

# Create your models here.

#Manager Class for UserProfile

class QuestionManager(models.Manager):
    def createQuestion(self,questionText):
        self.create(questionText=questionText)

class Question(models.Model):
    questionText = models.CharField(max_length = 300)
    objects = QuestionManager()

class AnswerManager(models.Manager):
    def createAnswer(self, question, answerText):
        self.create(question=question,answerText=answerText)
         

class Answer(models.Model):
      question = models.ForeignKey(Question, on_delete = models.SET_NULL, null = True)
      answerText = models.CharField(max_length = 300)     
      objects = AnswerManager()                  

class UserProfileManager(models.Manager):
    #create new userprofile if not existed 
    def createUserProfile(self, username, chat_url, first_name, last_name, email, created_on, role):
        userProfile = UserProfile.objects.hasUserProfile(username__exact=username, chat_url__exact=chat_url)
        if (not userProfile):
            userProfile = self.create(username=username, chat_url=chat_url, first_name=first_name, 
                                        last_name=last_name, email=email, created_on=created_on, role=role)
        return userProfile    
    
    def hasUserProfile(self, username, chat_url):
        try:
            userProfile = UserProfile.objects.get(username__iexact=username, chat_url__iexact=chat_url)
            return userProfile
        except MultipleObjectsReturned:
            print ("More than one user with the same username and chat_url.")
            return None
        except DoesNotExist:
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
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    email = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    role = models.CharField(max_length = 40)
    objects = UserProfileManager()

    def __str__(self):
        return self.username

class AttendanceManager(models.Manager):
    def createAttendance(self, created_by, created_on):
        attendance=self.create(created_by=created_by,created_on=created_on)
        return attendance.id

    def getAttendanceByID(self, attendanceID):
        try:
            attendance = Attendance.objects.get(id__exact=attendanceID)
            return attendance
        except MultipleObjectsReturned:
            print ("More than one objects with the same username and chat_url.")
            return None
        except DoesNotExist:
            print ("Object does not exist.")
            return None   


class Attendance(models.Model):
    created_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
    created_on = models.DateTimeField(auto_now_add = True)
    objects = AttendanceManager()    

class AttendanceSubmitManager(models.Model):
    def createAttendanceSubmit(self, attendance, submitted_on, username, chat_url,
                                first_name, last_name, email, created_on, role):

        submitted_by = UserProfile.objects.createUserProfile(username=username, chat_url=chat_url, 
                                                     first_name=first_name, last_name=last_name,
                                                     email=email, created_on=created_on, role=role) 

        attendanceSubmit = self.create(attendance=attendance, submitted_on=submitted_on, submitted_by=submitted_by)
        return attendanceSubmit.id

    def createAttSubmit(self, attendance, submitted_on, submitted_by):
        submission = self.create(attendance=attendance, submitted_on=submitted_on, submitted_by=submitted_by)   
        return submission.id

    def getSubmissionList(self, attendance):
        try :
            submissionList = self.filter(attendance__id__exact=attendance.id)
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
    objects = AttendanceSubmitManager()

            


