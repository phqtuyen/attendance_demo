from django.urls import path
from . import views
from .views import *
import socket

view = AppViews()
urlpatterns = [
    path('', view.createForm, name='create'),
    path('submit', view.submit, name='submit'),
    path('submitResult', view.submitResult, name='submitResult'),
    path('view', view.view, name='view'),
]