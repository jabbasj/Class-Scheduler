from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

from django.core import serializers

def schedule(request):
    """Renders the schedule page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        return post_handler(request)

    else:
        if request.session['semester'] != None and request.session['year'] != None:
            return post_handler(request)

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


def post_handler(request):
    
    chosen_semester = None
    chosen_year = None
    student = None
    # how will we distinguish between courses registered and courses to simply view on a schedule?
    # for now, let's use grade = '##' to mean that this course is not registered, just pending confirmation
    courses_registered = []

    if 'view' in request.POST.keys():
        chosen_semester = request.POST.get('semester')
        chosen_year = request.POST.get('year')
        request.session['year'] = chosen_year
        request.session['semester'] = chosen_semester
        try:
            student = Students.objects.get(email=request.user)
            registered = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=chosen_year, finished = False)

            for reg in registered:
                courses_registered.append(Courses.objects.get(cid=reg.cid, sid=reg.sectionid, semester=chosen_semester, year=chosen_year, type=reg.type))

        except Exception as e:
            courses_registered = None
    else:
        chosen_semester = request.session['semester']
        chosen_year = request.session['year']

        try:
            student = Students.objects.get(email=request.user)
            registered = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=chosen_year, finished = False)

            for reg in registered:
                courses_registered.append(Courses.objects.get(cid=reg.cid, sid=reg.sectionid, semester=chosen_semester, year=chosen_year, type=reg.type))

        except Exception as e:
            courses_registered = None


    return render(
        request,
        'schedule/schedule.html',
        context_instance = RequestContext(request,
        {
            'title':'Schedule',
            'chosen_semester': chosen_semester,
            'chosen_year': chosen_year,
            'courses_registered': courses_registered,
            'json_courses_registered': serializers.serialize('json',courses_registered, use_natural_foreign_keys = True),
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )
