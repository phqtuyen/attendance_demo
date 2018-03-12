from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.template import loader
from django.http import HttpResponse


#### Attendance API
####   Create, View, Delete Attendance

#### Attendance Check API
####   Add new attendance check, create a user, create an attendance check (that link between user and attendance)

class ConfirmFormSerializer(serializers.Serializer):
	def to_internal_value(self, data):
		return {
		}

	def to_representation(self, obj):
		return {
			'is_success': 'Attendance Form is created'
		}


class CreateFormSerializer(serializers.Serializer):
	def to_internal_value(self, data):
		return {
		}

	def to_representation(self, obj):
		html = loader.get_template("views/create.html")
		response = HttpResponse(html.render())
		return {
			'html': response.getvalue()
		}

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
