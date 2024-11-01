from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    object_id = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['object_id', 'title', 'course_code', 'university', 'description', 'file', 'status']
        extra_kwargs = {
            'title': {'required': True},
            'course_code': {'required': True},
            'university': {'required': True},
            'description': {'required': True},
            'status': {'required': True}, 
        }

    def get_object_id(self, obj):
        # Convert the ObjectId to a string
        return str(obj._id)


