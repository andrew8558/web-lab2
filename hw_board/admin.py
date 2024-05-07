from django.contrib import admin
from .models import Course, HomeworkType, Student, HwDone
# Register your models here.

admin.site.register(Course)
admin.site.register(HomeworkType)
admin.site.register(HwDone)
admin.site.register(Student)
