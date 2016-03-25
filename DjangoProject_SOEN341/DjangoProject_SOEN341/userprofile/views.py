from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

def profile(request):
    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    student = None
    if (request.user.is_authenticated()):
        student = Students.objects.get(email=request.user)
    return render(
        request,
        'userprofile/profile.html',
        context_instance = RequestContext(request,
        {
            'title':'Profile',
            'student': student,
            'date':datetime.now(),
            'year':datetime.now().year,
        })
    )
