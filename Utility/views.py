from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseServerError
from django.template import loader, RequestContext
from attendance_app.models import UserProfile
from Utility.default_data.rocket_data import RCRole

# Create your views here.

class AbstractControllers:

    def get_role(self, st):
        if st is None:
            return RCRole.USER
        if RCRole.ADMIN in st:
            return RCRole.ADMIN
        else:
            return RCRole.USER

    def userProfileFromRequest(self, params):
        temp_profile = UserProfile()\
                                        .configID(params.get('username').strip(), params.get('source').strip())\
                                        .configName(params.get('name').strip())\
                                        .configEmail(params.get('email').strip(),
                                        self.get_role(params.get('role').strip()))\
                                        .configCreatedOn(None)
        return temp_profile

    def createUserProfileIfNeeded(self, params):
        temp_prof = self.userProfileFromRequest(params)
        user_prof = UserProfile.objects.createUserProfile(temp_prof)
        return user_prof

    def isAdmin(self, params):
        username = params.get('username')
        source = params.get('source')
        print('check is admin:')
        print('username: ', username, 'source: ', source)
        admin = UserProfile.objects.hasUserWithRole(username,
                                                                                                source,
                                                                                                RCRole.ADMIN)
        print('All users: ',UserProfile.objects.all())
        return admin
