from django.urls import path
from . import views
from .views import *
import socket
from feedback.feedback_api_view import *
from feedback.views import *

view = GeneralView()
api_view = FeedbackAPIView()
urlpatterns = [
	path('confirm_create_feedback', api_view.confirm_create_feedback,
			name = 'confirm_create_feedback'),
	path('further_comment', view.further_comment,
			name = 'further_comment'),
	path('confirm_submit', api_view.confirm_submit,
			name = 'confirm_submit')
]