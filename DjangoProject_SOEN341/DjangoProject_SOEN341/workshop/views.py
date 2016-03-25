from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

def workshop(request):
    """Renders the workshop page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'workshop/workshop.html',
        context_instance = RequestContext(request,
        {
            'title':'Workshop',
            'suggested_sequence': Sequence.objects.all(),
            'prerequisites': Prerequisites.objects.all(),
            'message':'Your workshop page.',
            'year':datetime.now().year,
        })
    )
