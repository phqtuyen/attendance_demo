from django.db import models
from attendance_app.models import UserProfile, QuizSession, QuizSessionManager, StudentSubmission, StudentSubmissionManager

class FeedbackSessionManager(QuizSessionManager):
	pass

class FeedbackSession(QuizSession):
    
    objects = FeedbackSessionManager()  

class StudentFeedbackManager(StudentSubmissionManager):
    def create_student_feedback(self, attendance, tempProfile):

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

    def get_feedback_list(self, attendance):
        try :
            submissionList = self.filter(attendance__id__exact = attendance.id)
            if (not submissionList):
                return None
            else:
                return submissionList    
        except Exception:
            print (Exception)    
            return None	

class StudentFeedback(StudentSubmission):
    feedback_session = models.ForeignKey(FeedbackSession, on_delete = models.SET_NULL, null = True)
    student_choice = models.CharField(max_length = 255)
    student_comment = models.CharField(max_length = 500)
    objects = StudentFeedbackManager()
# Create your models here.
