from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

def schedule(request):
    """Renders the schedule page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'schedule/schedule.html',
        context_instance = RequestContext(request,
        {
            'title':'Schedule',
            'timeslots': Timeslots.objects.all(),
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )
