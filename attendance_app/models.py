from django.db import models

# Create your models here.

#Manager Class for UserProfile

class QuestionManager(models.Manager):
    def createQuestion(self,questionText):
        if (not Question.objects.filter(questionText__iexact=questionText)):
            self.create(questionText=questionText)

class Question(models.Model):
    questionText = models.CharField(max_length = 300)
    objects = QuestionManager()

class AnswerManager(models.Manager):
    def createAnswer(self, question, answerText):
        if (not Answer.objects.filter(answerText__iexact=answerText)):
            self.create(question=question,answerText=answerText)

class Answer(models.Model):
      question = models.ForeignKey(Question, on_delete = models.SET_NULL, null = True)
      answerText = models.CharField(max_length = 300)     
                        

class UserProfileManager(models.Manager):
    #create new userprofile if not existed 
    def createUserProfile(self, username, chat_url, first_name, last_name, email, created_on, role):
        userProfile = UserProfile.objects.filter(username__exact=username, chat_url__exact=chat_url)
        if (not userProfile):
            userProfile = self.create(username=username, chat_url=chat_url, first_name=first_name, 
                                        last_name=last_name, email=email, created_on=created_on, role=role)
            userProfile.save()
            return userProfile
        else :
            return userProfile    


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
        attendance.save()
        return attendance.id

class Attendance(models.Model):
	created_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
	created_on = models.DateTimeField(auto_now_add = True)
    #objects = AttendanceManager()    

class AttendanceSubmitManager(models.Model):
    def createAttendanceSubmit(self, attendance, submitted_on, username, chat_url):
        user = UserProfile.objects.createUserProfile(username=username, chat_url=chat_url, 
                                                     firstname="", last_name="",
                                                     email="", created_on="",role="student") 

        attendanceSubmit = self.create(attendance=attendance, submitted_on=submitted_on, submitted_by=submitted_by)


class AttendanceSubmit(models.Model):
	attendance = models.ForeignKey(Attendance, on_delete = models.SET_NULL, null = True)
	submitted_on = models.DateTimeField(auto_now_add = True)	
	submitted_by = models.ForeignKey(UserProfile, on_delete = models.SET_NULL, null = True)
    #objects = AttendanceSubmitManager()

            


