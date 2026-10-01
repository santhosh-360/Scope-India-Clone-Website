from django.contrib import admin

# Register your models here.
from .models import Contact,Student,Course,Enrollment

admin.site.register(Contact)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
