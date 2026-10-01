from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    hobbies = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    password = models.CharField(max_length=128)
    email_verified = models.BooleanField(default=False)
    verification_token=models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    is_first_login=models.BooleanField(default=True)
    # verification_token = models.CharField(max_length=255, blank=True, null=True)
    # temp_password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
     return self.course_name



# class Enrollment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     signed_up_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student.username} - {self.course.course_name}"

class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    signed_up_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.course.course_name}"