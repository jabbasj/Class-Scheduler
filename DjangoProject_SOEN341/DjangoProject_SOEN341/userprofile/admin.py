from django.contrib import admin
from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots, AuthUser

# Register your models here.

# doing everything here cause yolo
admin.site.register(Students)
admin.site.register(Sequence)
admin.site.register(Registered)
admin.site.register(Courses)
admin.site.register(Prerequisites)
admin.site.register(Timeslots)
