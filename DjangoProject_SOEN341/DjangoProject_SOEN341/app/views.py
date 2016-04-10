"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

from django.utils.encoding import smart_str
from django.http import HttpResponse

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        return download_user_manual(request)

    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )


def download_user_manual(request):
    location = 'app/static/app/content/user_manual.pdf'
    file = open(location, 'rb')
    content = file.read()
    file.close

    #serve the file
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=user_manual.pdf'

    return response
