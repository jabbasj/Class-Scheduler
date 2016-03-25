from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

def record(request):
    """Renders the academic record page."""
    assert isinstance(request, HttpRequest)
    completed_courses = None
    if (request.user.is_authenticated()):
        completed_courses = Registered.objects.filter(studentid = Students.objects.get(email=request.user).sid, finished = True)

    return render(
        request,
        'record/records.html',
        context_instance = RequestContext(request,
        {
            'title':'Academic Record',
            'completed_courses': completed_courses,
            'year':datetime.now().year,
        })
    )
