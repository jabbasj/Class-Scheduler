from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

from django.core import serializers
from django.core.cache import cache

def schedule(request):
    """Renders the schedule page."""
    assert isinstance(request, HttpRequest)

    if (request.user.is_authenticated()):
        return post_handler(request)

    return render(
        request,
        'schedule/schedule.html',
        context_instance = RequestContext(request,
        {
            'title':'Schedule',
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )


def post_handler(request):

    chosen_semester = None
    chosen_year = None
    student = None

    courses_registered = []
    potential_courses = []
    potential_courses_success = None

    lectures = []
    tutorials = []
    labs = []

    if 'search' in request.POST.keys():
        potential_courses = search(request)
        if len(potential_courses) > 0:
            potential_courses_success = True
            cache.set('potentialcourses', potential_courses)
        else:
            potential_courses_success = False

    if 'check_sections' in request.POST.keys():
        lectures, tutorials, labs = get_available_sections(request)

        potential_courses = cached_queries('potentialcourses')['cache']
        if potential_courses != None and len(potential_courses) > 0:
            potential_courses_success = True
        else:
            potential_courses_success = False
        
        # render modal with [ lecture sections | tutorial sections | lab sections ] available for chosen course
        # user checks from each, submits... conflicts will be checked, success or fail message.
        
    chosen_semester, chosen_year, courses_registered = get_registered_courses(request)
        
    return render(
        request,
        'schedule/schedule.html',
        context_instance = RequestContext(request,
        {
            'title':'Schedule',
            'chosen_semester': chosen_semester,
            'chosen_year': chosen_year,
            'json_lectures': json_serialize(lectures),
            'json_tutorials': json_serialize(tutorials),
            'json_labs': json_serialize(labs),
            'lectures': lectures,
            'tutorials': tutorials,
            'labs': labs,
            'json_courses_registered': json_serialize(courses_registered),
            'potential_courses' : potential_courses,
            'potential_courses_success': potential_courses_success,
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )

def get_available_sections(request):

    lectures = []
    tutorials = []
    labs = []

    chosen_semester = request.session['semester']            
    chosen_year = request.session['year']

    course_id = request.POST.get('check_sections')

    try:
        lectures = get_sections_available_to_student(request, 'lec', course_id, False)
        tutorials = get_sections_available_to_student(request, 'tut', course_id, False)
        labs = get_sections_available_to_student(request, 'lab', course_id, False)

    except Exception as e:
        lectures = []
        tutorials = []
        labs = []

    return lectures, tutorials, labs

def get_registered_courses(request):
    chosen_semester = None
    chosen_year = None
    student = None
    courses_registered = []

    if 'view' in request.POST.keys():
        chosen_semester = request.POST.get('semester')
        chosen_year = request.POST.get('year')
        request.session['year'] = chosen_year
        request.session['semester'] = chosen_semester

    elif 'semester' in request.session and 'year' in request.session: 

        chosen_semester = request.session['semester']            
        chosen_year = request.session['year']
        
    try:            
        student = Students.objects.get(email=request.user)            
        registered = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=chosen_year, finished = False)
            
        for reg in registered:                
            courses_registered.append(Courses.objects.get(cid=reg.cid, sid=reg.sectionid, semester=chosen_semester, year=chosen_year, type=reg.type))
        
    except Exception as e:            
        courses_registered = []

    return chosen_semester, chosen_year, courses_registered


def search(request):
    return get_sections_available_to_student(request)


def get_sections_available_to_student(request, type_chosen = 'lec', course_id_specified = None, unique = True):
    chosen_semester = None
    chosen_year = None
    courses_registered = []
    courses_available = []
    unique_lectures = []

    chosen_semester, chosen_year, courses_registered = get_registered_courses(request)

    try:
        if course_id_specified == None:                
            courses_available = Courses.objects.filter(semester=chosen_semester, year=int(chosen_year), type=type_chosen)
        else:                
            courses_available = Courses.objects.filter(cid=Sequence.objects.get(cid=course_id_specified).cid, semester=chosen_semester, year=int(chosen_year), type=type_chosen)
        
        seen = []
        for i in courses_available:
            if unique == True:
                if i.cid not in seen:    	        
                    unique_lectures.append(i)
                    seen.append(i.cid)
            else:
                #get all
                unique_lectures.append(i)

        if len(unique_lectures) > 0:
            courses_not_full = []
            courses_not_full = remove_full_courses(request, unique_lectures)

            if len(courses_not_full) > 0:                 
                courses_not_currently_registered = []                        
                courses_not_currently_registered = remove_currently_registered(request, courses_not_full)
                

                if len(courses_not_currently_registered) > 0:
                    courses_not_already_done = []
                    courses_not_already_done = remove_completed_by_student(request, courses_not_currently_registered)

                    if len(courses_not_already_done) > 0:
                        courses_prereqs_met = []
                        courses_prereqs_met = remove_prereqs_missing(request, courses_not_already_done)
                        courses_available = courses_prereqs_met

    except Exception as e:
        courses_available = []

    return courses_available


def remove_completed_by_student(request, courses):
    not_completed_yet = []

    if (courses != None):
        try:
            for i in courses:
                if check_if_course_passed(request, courses) == False:
                    not_completed_yet.append(i)

        except Exception as e:
            not_completed_yet = []

    return not_completed_yet


def discover_prerequisite_classes(cid):
    discovered_classes = []

    if len(discovered_classes) == 0:
        first = Prerequisites.objects.filter(pid = cid)
        for k in first:
            discovered_classes.append(k.rid)

    for i in discovered_classes:
        potentially_new = Prerequisites.objects.filter(pid = i)
        for j in potentially_new:
            if j not in discovered_classes:
                discovered_classes.append(j.rid)
    return discovered_classes


#altid / parallel not considered
def remove_prereqs_missing(request, courses):
    courses_prereqs_satisfied = []

    try:
        for i in courses:
            has_prerequisites = []
            prereqs_passed = True
            has_prerequisites = (Prerequisites.objects.filter(pid = i.cid.cid))

            if len(has_prerequisites) > 0:
                all_prereqs = discover_prerequisite_classes(i.cid.cid)
                for j in all_prereqs:                            
                    prereqs_passed = check_if_course_passed(request, j)     
                               
                    if prereqs_passed == False:                        
                        break

            if prereqs_passed:
                courses_prereqs_satisfied.append(i)


    except Exception as e:
        courses_prereqs_satisfied = []


    return courses_prereqs_satisfied


def check_if_course_passed(request, courseid):
    try:
        finished_course = Registered.objects.get(cid=courseid, studentid = Students.objects.get(email=request.user).sid, finished = True, type = 'lec') 
        if finished_course != None and int(finished_course.grade) >= 50:
            return True
    except Exception as e:
        return False
    return False


def remove_currently_registered(request, courses):
    not_already_registered = []

    try:
        currently_registered = []
        currently_registered = Registered.objects.filter(studentid = Students.objects.get(email=request.user).sid, finished = False, type = 'lec')
        if len(currently_registered) > 0:
            currently_registered_cids = get_cids(currently_registered)

            for i in courses:
                if i.cid.cid not in currently_registered_cids:
                    not_already_registered.append(i)

    except Exception as e:
        not_already_registered = []

    return not_already_registered


def remove_full_courses(request, courses):
    courses_with_capacity = []

    for i in courses:
        if i.capacity > 0:
            courses_with_capacity.append(i)

    return courses_with_capacity


def get_cids(courses):
    cids_list = []
    for i in courses:
        cids_list.append(i.cid)
    return cids_list


def json_serialize(courses):
    #if (courses != None) and len(courses) > 0:
    return serializers.serialize('json',courses, use_natural_foreign_keys = True)
    #return []

def cached_queries(key):
    return {'cache': cache.get(key)}


