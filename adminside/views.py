from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .serializers import UserLoginSerializer, CourseSerializer
from .models import Course
from rest_framework import generics
from pymongo import MongoClient
from bson import json_util
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from rest_framework.permissions import IsAuthenticated

class LoginAPIView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Generate access and refresh tokens
                access_token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access': str(access_token),
                    'refresh': str(refresh_token),
                })
            else:
                return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCourseAPIView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Course added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DraftCoursesAPIView(APIView):
#     def get(self, request):
#         draft_courses = Course.objects.filter(status=Course.DRAFT)
#         serializer = CourseSerializer(draft_courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class PublishedCoursesAPIView(APIView):
#     def get(self, request):
#         published_courses = Course.objects.filter(status=Course.PUBLISHED)
#         serializer = CourseSerializer(published_courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.renderers import JSONRenderer
class DraftCoursesAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        draft_courses = Course.objects.filter(status=Course.DRAFT)
        serializer = CourseSerializer(draft_courses, many=True)
        return Response({'draft': serializer.data}, status=status.HTTP_200_OK)

class PublishedCoursesAPIView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        published_courses = Course.objects.filter(status=Course.PUBLISHED)
        serializer = CourseSerializer(published_courses, many=True)
        return Response({'published': serializer.data}, status=status.HTTP_200_OK)


class DeleteCourseAPIView(APIView):
    """
    API view to delete a course by ID.
    """
    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)  # Fetch the course by primary key
            course.delete()  # Delete the course
            return Response({'message': 'Course deleted successfully'}, status=status.HTTP_200_OK)  # Change to 200 OK
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateCourseAPIView(APIView):
    """
    API view to update a course by ID.
    """
    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)  # Fetch course by ID
            serializer = CourseSerializer(course, data=request.data)  # Replace all data
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)  # Fetch course by ID
            serializer = CourseSerializer(course, data=request.data, partial=True)  # Update only provided fields
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)
        print(f"Requested status: {status}") 
        if status:
            status = status.strip()
            queryset = queryset.filter(status=status)
        print(f"Filtered queryset: {queryset}")  
        return queryset
    


class ToggleCourseStatusAPIView(APIView):
    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            if course.status == Course.DRAFT:
                course.status = Course.PUBLISHED
            else:
                course.status = Course.DRAFT
            course.save()
            return Response({'message': f'Course status changed to {course.status}'}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        


# blacklisted_tokens = set()

# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         auth_header = request.headers.get('Authorization', '')
#         token = auth_header.split(' ')[1] if auth_header else None

#         if token:

#             blacklisted_tokens.add(token)
#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'detail': 'Token missing'}, status=status.HTTP_400_BAD_REQUEST)
        

