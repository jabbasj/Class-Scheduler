from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

def schedule(request):
    """Renders the schedule page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
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
    student = Students.objects.get(email=request.user)
    # how will we distinguish between courses registered and courses to simply view on a schedule?
    # for now, let's use grade = '##' to mean that this course is not registered, just pending confirmation
    courses_registered = None
    courses_pending_confirmation = None

    if 'view' in request.POST.keys():
        chosen_semester = request.POST.get('semester')
        chosen_year = request.POST.get('year')
        courses_registered = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=chosen_year, finished = False)
        courses_pending_confirmation = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=chosen_year, grade = '##')

    return render(
        request,
        'schedule/schedule.html',
        context_instance = RequestContext(request,
        {
            'title':'Schedule',
            'chosen_semester': chosen_semester,
            'chosen_year': chosen_year,
            'courses_registered': courses_registered,
            'courses_pending_confirmation': courses_pending_confirmation,
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )
