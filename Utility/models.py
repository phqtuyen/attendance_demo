from django.db import models

# Create your models here.


class RocketAPIAuthenticationManager(models.Manager):
    def createRocketAPIAuth(self, url, user_id, auth_token):
        api_authentication = self.create(rocket_chat_url = url, 
                                    rocket_chat_user_id = user_id, 
                                    rocket_chat_auth_token = auth_token)   
        api_authentication.save()
        return api_authentication.id


    def getRocketAPIAuth(self, url):
        try:
            api_authentication = RocketAPIAuthentication.objects.get(rocket_chat_url__exact = url)
            return api_authentication
        except MultipleObjectsReturned:
            print ("More than one objects with the same username and chat_url.")
            return None
        except ObjectDoesNotExist:
            print ("Object does not exist.")
            return None               


class RocketAPIAuthentication(models.Model):
    rocket_chat_user_id = models.CharField(max_length = 100)
    rocket_chat_auth_token = models.CharField(max_length = 150)
    rocket_chat_url = models.CharField(max_length = 255)

    objects = RocketAPIAuthenticationManager()

    def get_user_id(self):
        return self.rocket_chat_user_id

    def get_auth_token(self):
        return self.rocket_chat_auth_token

    def get_url(self):
        return self.rocket_chat_url

    def set_user_id(self, uid):
        self.rocket_chat_user_id = uid
        #self.save()
        return self

    def set_auth_token(self, token):
        self.rocket_chat_auth_token = token
        #self.save()
        return self

    def set_url(self, url):
        self.rocket_chat_url = url
        #self.save()
        return self

