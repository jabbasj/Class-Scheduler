from django.contrib import admin
from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots, AuthUser
from django.db import models

# Register your models here.

class CoursesAdmin(admin.ModelAdmin):
    list_display = ('cid', 'sid', 'type', 'credits', 'lecturer', 'capacity', 'room',)
    search_fields = ['cid__cid', 'sid', 'type', 'credits', 'lecturer', 'capacity', 'room',]
    list_filter = ('type',)
    ordering = ('cid__cid',)

class RegisteredAdmin(admin.ModelAdmin):
    list_display = ('get_studentid', 'get_firstname', 'get_lastname', 'cid', 'sectionid', 'semester', 'year', 'grade', 'finished',)
    search_fields = ['studentid__sid', 'studentid__firstname', 'studentid__lastname', 'studentid__email', 'cid', 'sectionid', 'semester', 'year',]
    list_filter = ('semester', 'year',)

    def get_firstname(self, obj):
        return obj.studentid.firstname
    get_firstname.short_description = 'First Name'
    get_firstname.admin_order_field = 'firstname'

    def get_studentid(self, obj):
        return obj.studentid.sid
    get_studentid.short_description = 'Student ID'
    get_studentid.admin_order_field = 'studentid'

    def get_lastname(self, obj):
        return obj.studentid.lastname
    get_lastname.short_description = 'Last Name'
    get_lastname.admin_order_field = 'lastname'

class StudentsAdmin(admin.ModelAdmin):
    list_display = ('sid', 'firstname', 'lastname', 'email',)
    search_fields = ['sid', 'firstname', 'lastname', 'email',]
    ordering = ('sid',)

class SequenceAdmin(admin.ModelAdmin):
    list_display = ('cid', 'semester', 'year',)
    search_fields = ['cid', 'semester', 'year',]
    list_filter = ('semester', 'year',)
    ordering = ('year',)

class PrerequisitesAdmin(admin.ModelAdmin):
    list_display = ('pid', 'rid', 'parallel',)
    search_fields = ['pid', 'rid', 'parallel',]
    list_filter = ('parallel',)
    ordering = ('pid',)

class TimeslotsAdmin(admin.ModelAdmin):
    list_display = ('id', 'starthour', 'endhour', 'day',)
    search_fields = ['id', 'starthour', 'endhour', 'day',]

# doing everything here cause yolo
admin.site.register(Students, StudentsAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Registered, RegisteredAdmin)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(Prerequisites, PrerequisitesAdmin)
admin.site.register(Timeslots, TimeslotsAdmin)
