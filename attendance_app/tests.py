
from django.test import TestCase
from .models import Bucketlist

# Add these imports at the top
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from attendance_app.views import AppViews
from attendance_app.models import UserProfile, Attendance, AttendanceSubmit
from django.http import HttpResponse, HttpRequest
import requests

class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.bucketlist_name = "Write world class code"
        self.bucketlist = Bucketlist(name=self.bucketlist_name)

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count, new_count)



# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""


    def setUp(self):
    	self.app_view = AppViews()
    	self.host = 'http://127.0.0.1:8000/'
    	self.instructor_data = {'username': 'meomap', 
    							'chat_url': 'tuyen@gmail.com', 
    							'first_name': 'tuyen', 
    							'last_name': 'pham', 
    							'email': 'kootuyen@gmail.com', 
    							'role': 'instructor'}

    	self.student_data = {'username': 'meou', 'chat_url': 'meou@gmail.com', 'first_name': 'tuyen', 'last_name': 'pham', 'email': 'kootuyen@gmail.com', 'role': 'instructor'}						
    def test_createForm(self):
    	 
    	response = requests.post(self.host + 'attendance_app/', data=data)

		self.app_view     		




    # def setUp(self):
    #     """Define the test client and other test variables."""
    #     self.client = APIClient()
    #     self.bucketlist_data = {'name': 'Go to Ibiza'}
    #     self.response = self.client.post(
    #         reverse('create'),
    #         self.bucketlist_data,
    #         format="json")

    # def test_api_can_get_a_bucketlist(self):
    #     """Test the api can get a given bucketlist."""
    #     bucketlist = Bucketlist.objects.get()
    #     response = self.client.get(
    #         reverse('details',
    #         kwargs={'pk': bucketlist.id}), format="json")

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertContains(response, bucketlist)

    # def test_api_can_update_bucketlist(self):
    #     """Test the api can update a given bucketlist."""
    #     change_bucketlist = {'name': 'Something new'}
    #     res = self.client.put(
    #         reverse('details', kwargs={'pk': bucketlist.id}),
    #         change_bucketlist, format='json'
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_api_can_delete_bucketlist(self):
    #     """Test the api can delete a bucketlist."""
    #     bucketlist = Bucketlist.objects.get()
    #     response = self.client.delete(
    #         reverse('details', kwargs={'pk': bucketlist.id}),
    #         format='json',
    #         follow=True)

    #     self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
