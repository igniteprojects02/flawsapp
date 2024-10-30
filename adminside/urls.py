from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'), 
    path('add-course/', AddCourseAPIView.as_view(), name='add-course'),
    path('delete-course/<int:pk>/', DeleteCourseAPIView.as_view(), name='delete-course'),
    path('update-course/<int:pk>/', UpdateCourseAPIView.as_view(), name='update-course'),
    path('api/toggle-course-status/<int:pk>/', ToggleCourseStatusAPIView.as_view(), name='toggle-course-status'),

    # path('draft/<int:course_id>/', DraftCourseView.as_view(), name='draft_course'),
    path('courses/', CourseList.as_view(), name='course-list'),
    # path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('courses/draft/', DraftCoursesAPIView.as_view(), name='draft-courses'),
    path('courses/published/', PublishedCoursesAPIView.as_view(), name='published-courses'),
    


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
