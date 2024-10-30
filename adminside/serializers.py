from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'course_code', 'university', 'description', 'file', 'status']
        extra_kwargs = {
            'title': {'required': True},
            'course_code': {'required': True},
            'university': {'required': True},
            'description': {'required': True},
            'status': {'required': True}, 
        }
    def get_status(self, obj):
        return obj.status  

