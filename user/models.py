from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your models here.

#Manager Class for UserProfile         

class UserProfileManager(models.Manager):
    #create new userprofile if not existed 
    def createUserProfile(self, tempProfile):
        userProfile = UserProfile.objects.hasUserProfile(username=tempProfile.username, 
                                                            chat_url=tempProfile.chat_url)
        if (not userProfile):
            userProfile = self.create(username=tempProfile.username,
                                         chat_url=tempProfile.chat_url)
            userProfile.configFromProfile(tempProfile)
            userProfile.save()
        return userProfile    

    
    def hasUserProfile(self, username, chat_url):
        try:
            userProfile = UserProfile.objects.get(username__iexact = username, chat_url__iexact = chat_url)
            return userProfile
        except MultipleObjectsReturned:
            print ("More than one user with the same username and chat_url.")
            return None
        except ObjectDoesNotExist:
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
    name = models.CharField(max_length = 150)
    email = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    role = models.CharField(max_length = 40)
    objects = UserProfileManager()

    def configID(self, username, chat_url):
        self.username = (username or "").strip()
        self.chat_url = (chat_url or "").strip()
        return self

    def configName(self, name):
        self.name = (name or "").strip()
        return self    
        
    def configEmail(self, email, role):
        self.email = (email or "").strip()
        self.role = (role or "").strip()
        return self

    def configCreatedOn(self, created_on):
        if (created_on):
            self.created_on = created_on
        else:
            self.created_on = timezone.now()
        return self    

    def configFromProfile(self, tempProfile):
        self.name = tempProfile.name 
        self.email = tempProfile.email
        self.role = tempProfile.role
        self.created_on = tempProfile.created_on or timezone.now()
        self.save()
        return self

    def __str__(self):
        return self.username + ' ' + self.name + ' ' + self.email + ' ' + self.role
