"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
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

def profile(request):
    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/profile.html',
        context_instance = RequestContext(request,
        {
            'title':'Profile',
            'student_name': Students.objects.get(email=request.user),
            'message':'Your student profile page.',
            'year':datetime.now().year,
        })
    )

def record(request):
    """Renders the academic record page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/records.html',
        context_instance = RequestContext(request,
        {
            'title':'Academic Record',
            'message':'Your student record page.',
            'year':datetime.now().year,
        })
    )

def schedule(request):
    """Renders the schedule page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/schedule.html',
        context_instance = RequestContext(request,
        {
            'title':'Schedule',
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )

def workshop(request):
    """Renders the workshop page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/workshop.html',
        context_instance = RequestContext(request,
        {
            'title':'Workshop',
            'message':'Your workshop page.',
            'year':datetime.now().year,
        })
    )
