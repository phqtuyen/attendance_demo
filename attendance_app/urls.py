from django.urls import path
from . import views
from .views import *
from .api_views import *
import socket

view = AppViews()
api_view = APIViews()
urlpatterns = [
	path('html/', view.createAttendance, name='htmlCreateAttendance'),
	path('html/create_attendance', view.createAttendance, name='htmlCreateAttendance'),
    path('html/confirm_create_attendance', view.confirmCreateAttendance, name='htmlConfirmCreateAttendance'),
    path('html/confirm_submit', view.confirmSubmit, name='htmlConfirmSubmit'),
    path('html/view_attendance', view.viewAttendance, name='htmlViewAttendance'),
    path('create_attendance', api_view.createAttendance, name='apiCreateAttendance'),
    path('confirm_create_attendance', api_view.confirmCreateAttendance, name='apiConfirmCreateAttendance'),
    path('confirm_submit', api_view.confirmSubmit, name='apiConfirmSubmit'),
    path('view_attendance', api_view.viewAttendance, name='apiViewAttendance'),
]