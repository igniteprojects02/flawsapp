from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass



from djongo import models
from bson import ObjectId

class Course(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    title = models.CharField(max_length=255)
    course_code = models.CharField(max_length=50)
    university = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='courses_files/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    class Meta:
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title
