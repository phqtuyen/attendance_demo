from django.db import models
from attendance_app.models import UserProfile, QuizSession, QuizSessionManager, StudentSubmission, StudentSubmissionManager
from django.utils import timezone

MAX_NUM_CHOICES = 3
DEFAULT_COMMENT = ''
DEFAULT = 1

class FeedbackSessionManager(QuizSessionManager):
    pass

class FeedbackSession(QuizSession):
    
    objects = FeedbackSessionManager()  

class StudentFeedbackManager(StudentSubmissionManager):
    def create_student_feedback(self, attendance, tempProfile):

        submitted_by = UserProfile.objects.createUserProfile(tempProfile) 
        submitted_by_list = self.student_submitted(submitted_by, attendance)
        if (not submitted_by_list):
            attendanceSubmit = self.create(feedback_session = attendance, 
                                            submitted_on = timezone.now(), 
                                            submitted_by = submitted_by,
                                            student_choice = DEFAULT,
                                            student_comment = DEFAULT_COMMENT)
            attendanceSubmit.save()
            return attendanceSubmit

        return submitted_by_list[0]               
           
    def student_submitted(self, submitted_by, feedback_session):
        try :
            submissionList = self.filter(submitted_by__id__exact = submitted_by.id,
                                            feedback_session__id__exact = feedback_session.id)
            if (not submissionList):
                return None
            else:
                return submissionList    
        except Exception:
            print (Exception)    
            return None        

    def get_feedback_list(self, feedback_session_id):
        try :
            submissionList = self.filter(feedback_session__id__exact = feedback_session_id)
            if (not submissionList):
                return None
            else:
                return submissionList    
        except Exception:
            print (Exception)    
            return None	

    def calc_num_choice(self, choice, feedback_session_id):
        return len(self.filter(feedback_session__id__exact = feedback_session_id,
                         student_choice__exact = choice))

    def calc_total(self, feedback_session_id):
        return len(self.filter(feedback_session__id__exact = feedback_session_id))

    def calc_ratio_of_choice(self, choice, feedback_session_id):
        total = float(self.calc_total(feedback_session_id))
        num_choice = float(self.calc_number_of_this_choice(choice, 
                                                            feedback_session_id))
        return num_choice / total

    def has_submissions(self, feedback_session_id): 
        submission_list = self.get_feedback_list(feedback_session_id)
        if submission_list:
            return len(submission_list) > 0
        else:
            return False    

            
class StudentFeedback(StudentSubmission):
    #CHOICE_LIST = ((0, 'SAD'), (1, 'NEUTRAL'), (2, 'HAPPY'))
    feedback_session = models.ForeignKey(FeedbackSession, 
                        on_delete = models.SET_NULL, null = True)
    student_choice = models.IntegerField(default = DEFAULT)
    student_comment = models.CharField(max_length = 500)
    objects = StudentFeedbackManager()
# Create your models here.

    def set_choice(self, choice):
        self.student_choice = choice
        self.save()
        return self

    def set_comment(self, comment):
        self.student_comment = comment
        self.save()
        return self

