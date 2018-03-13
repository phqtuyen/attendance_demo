from django.urls import path
from . import views
from .views import *
import socket

view = AppViews()
api_view = APIViews()
urlpatterns = [
    path('', view.createForm, name='create'),
    path('submit', view.submit, name='submit'),
    path('submitResult', view.submitResult, name='submitResult'),
    path('view', view.view, name='view'),
    path('create_attendance', api_view.createAttendance, name='apiCreateAttendance'),
    path('confirm_create_attendance', api_view.confirmCreateAttendance, name='apiConfirmCreateAttendance'),
    path('confirm_submit', api_view.confirmSubmit, name='apiConfirmCreateAttendance'),
    path('view_attendance', api_view.viewAttendance, name='apiViewAttendance'),
]