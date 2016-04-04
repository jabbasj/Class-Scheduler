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
    combo_added_success = None

    courses_registered = []
    potential_courses = []
    conflicts = []
    new_registries = []
    potential_courses_success = None
    combo_registered_success = None

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

    if 'register_combo' in request.POST.keys():
        combo_registered_success, conflicts, new_registries = register_lec_tut_lab_combo(request)

        if combo_registered_success == False:
            #since no changes, get the cache again
            potential_courses = cached_queries('potentialcourses')['cache']
            if potential_courses != None and len(potential_courses) > 0:
                potential_courses_success = True
            else:
                potential_courses_success = False
       
        
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
            'combo_registered_success': combo_registered_success,
            'conflicts': conflicts,
            'new_registries': new_registries,
            'message':'Your schedule page.',
            'year':datetime.now().year,
        })
    )

def register_lec_tut_lab_combo(request):

    combo_registered_success = None
    new_registries = []
    conflicts = []

    course_id = request.POST.get('register_combo')
    lec_section_id = request.POST.get('lec')
    tut_section_id = request.POST.get('tut')
    lab_section_id = request.POST.get('lab')

    lec = None
    tut = None
    lab = None

    try:
        lec = get_sections_available_to_student(request, 'lec', course_id, True, lec_section_id)
        tut = get_sections_available_to_student(request, 'tut', course_id, True, tut_section_id)
        lab = get_sections_available_to_student(request, 'lab', course_id, True, lab_section_id)

        # check if sections available but user didn't select one
        if len(lec) == 1 and lec_section_id == None:
            combo_registered_success = False

        if len(tut) == 1 and tut_section_id == None:                
            combo_registered_success = False

        if len(lab) == 1 and lab_section_id == None:                    
            combo_registered_success = False

        if combo_registered_success != False:
            combo_registered_success, conflicts, new_registries = check_conflicts_and_register_student_to(request, lec, lab, tut)

            if combo_registered_success and len(conflicts) == 0 and len(new_registries) > 0:
                combo_registered_success = True

    except Exception as e:
        combo_registered_success = False

    return combo_registered_success, conflicts, new_registries


def max_credits_registered(lec, courses_registered, MAX = 12):
    try:
        total_credits_registered = 0

        for reg in courses_registered:
            total_credits_registered += reg.credits

        total_credits_registered += lec.credits

        if total_credits_registered > MAX:
            return True
        else:
            return False

    except Exception as e:
        return True

    return True


def check_conflicts_and_register_student_to(request, lec, lab, tut):
    success = None
    conflicts = []
    new_registeries = []

    try:
        chosen_semester, chosen_year, courses_registered = get_registered_courses(request)

        if len(courses_registered) >= 0:
            # check conflicts
                
            if not isAvail(lec, courses_registered):                    
                success = False                    
                conflicts.append(lec)
                
            if not isAvail(tut, courses_registered):                    
                success = False                    
                conflicts.append(tut)
            
            if not isAvail(lab, courses_registered):                    
                success = False                    
                conflicts.append(lab)

            if success != False:
                # register
                if len(lec) == 1 and max_credits_registered(lec[0], courses_registered) == False:
                    lec = lec[0]
                else:
                    lec = None
                if len(tut) == 1:
                    tut = tut[0]
                else:
                    tut = None
                if len(lab) == 1:
                    lab = lab[0]
                else:
                    lab = None

                success, new_registeries = register_student_to(request, lec, tut, lab, chosen_semester, chosen_year)

    except Exception as e:
        success = False

    return success, conflicts, new_registeries

def register_student_to(request, lec, tut, lab, semester, year):
    success = False
    new_registery = []
    student = Students.objects.get(email=request.user)
    try:
        if lec != None:
            new_registery.append(Registered.create(student, lec.cid.cid, lec.sid, semester, year,lec.type,'', False ))
            success = True

            if success == True and tut != None:
                new_registery.append(Registered.create(student, tut.cid.cid, tut.sid, semester, year,tut.type,'', False ))
                success = True

            if success == True and lab != None:
                new_registery.append(Registered.create(student, lab.cid.cid, lab.sid, semester, year,lab.type,'', False ))
                success = True

    except Exception as e:
        success = False

    return success, new_registery

# computes time conflicts between given new_course and given 'registered' course list
def isAvail(new_course, registered):
    if len(new_course) > 0:
        new = new_course[0]

        try:
            if new.timeslot1.day == 0 and new.timeslot2.day == 0:
                return True # new class is online

            for reg in registered:
                if reg.timeslot1.day == 0 and reg.timeslot2.day == 0:
                    return True # both days online

                if new.timeslot1.day != 0:

                    if new.timeslot1.day == reg.timeslot1.day:

                        if reg.timeslot1.starthour <= new.timeslot1.starthour <= reg.timeslot1.endhour :
                            return False
                        if reg.timeslot1.starthour <= new.timeslot1.endhour <= reg.timeslot1.endhour:
                            return False

                    if new.timeslot1.day == reg.timeslot2.day:

                        if reg.timeslot2.starthour <= new.timeslot1.starthour <= reg.timeslot2.endhour:
                            return False
                        if reg.timeslot2.starthour <= new.timeslot1.endhour <= reg.timeslot2.endhour:
                            return False

                if new.timeslot2.day != 0:

                    if new.timeslot2.day == reg.timeslot1.day:
                        if reg.timeslot1.starthour <= new.timeslot2.starthour <= reg.timeslot1.endhour:
                            return False
                        if reg.timeslot1.starthour <= new.timeslot2.endhour <= reg.timeslot1.endhour:
                            return False

                    if new.timeslot2.day == reg.timeslot2.day:

                        if reg.timeslot2.starthour <= new.timeslot2.starthour <= new.timeslot2.endhour:
                            return False
                        if reg.timeslot2.starthour <= new.timeslot2.endhour <= reg.timeslot2.endhour:
                            return False

        except Exception as e:
            return False

    return True

# fetches all the available lec, tut, lab sections for the student for the specified course
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

# fetches all the courses currently registered for a specified semester
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
            courses_registered.append(Courses.objects.get(cid=reg.cid, sid=reg.sectionid, type=reg.type)) #semester=chosen_semester, year=chosen_year
        
    except Exception as e:            
        courses_registered = []

    return chosen_semester, chosen_year, courses_registered


# gets all unique lectures available for the student to take for chosen semester  
def search(request):
    return get_sections_available_to_student(request)


# function for fetching lectures, tutorials and labs available to register for chosen semester
# if type_chosen is specified it looks for specified type
# if u specify unique, it gets only unique course_id
# if course_id_specified is given then it looks for sections related to that course
# if section_id_specified is given then it looks for sections with the given id
def get_sections_available_to_student(request, type_chosen = 'lec', course_id_specified = None, unique = True, section_id_specified = None):
    chosen_semester = None
    chosen_year = None
    courses_registered = []
    courses_available = []
    unique_courses = []

    chosen_semester, chosen_year, courses_registered = get_registered_courses(request)

    try:
        if course_id_specified == None:        
            courses_available = Courses.objects.filter(type=type_chosen, semester=chosen_semester, year=int(chosen_year)) #semester=chosen_semester, year=int(chosen_year),
            if len(courses_available) == 0:
                courses_available = Courses.objects.filter(type=type_chosen)
        else:
            if section_id_specified == None:                
                courses_available = Courses.objects.filter(cid=Sequence.objects.get(cid=course_id_specified).cid, year=int(chosen_year), semester=chosen_semester, type=type_chosen)# semester=chosen_semester, year=int(chosen_year)
                if len(courses_available) == 0:
                    courses_available = Courses.objects.filter(cid=Sequence.objects.get(cid=course_id_specified).cid, type=type_chosen)
            else:
                courses_available = Courses.objects.filter(cid=Sequence.objects.get(cid=course_id_specified).cid, sid=section_id_specified, semester=chosen_semester, year=int(chosen_year), type=type_chosen) #semester=chosen_semester, year=int(chosen_year)
                if len(courses_available) == 0:
                    courses_available = Courses.objects.filter(cid=Sequence.objects.get(cid=course_id_specified).cid, sid=section_id_specified, type=type_chosen)
        
        seen = []
        for i in courses_available:
            if unique == True:
                key = {'cid':i.cid,'type': i.type}
                if key not in seen:        
                    unique_courses.append(i)
                    seen.append(key)
                else: # duplicate, keep most recent year/sem
                    duplicate = None
                    dup_index = -1
                    for j in unique_courses:
                        dup_index += 1
                        if j.cid == i.cid and j.type == i.type:
                            duplicate = j
                            break
                    if i.year == duplicate.year:
                        if i.semester != duplicate.semester:
                            if i.semester == 'Winter':
                                del unique_courses[dup_index]
                                unique_courses.append(i)
                            elif i.semester == 'Fall' and duplicate.semester == 'Summer':
                                del unique_courses[dup_index]
                                unique_courses.append(i)                            
                    else:
                        if i.year > duplicate.year:
                            del unique_courses[dup_index]
                            unique_courses.append(i)                      
            else:
                #get all
                unique_courses.append(i)

        if len(unique_courses) > 0:
            courses_not_full = []
            courses_not_full = remove_full_courses(request, unique_courses)
            courses_available = courses_not_full

        if len(courses_available) > 0:               
            courses_not_currently_registered = []                  
            courses_not_currently_registered = remove_currently_registered(request, courses_not_full)                
            courses_available = courses_not_currently_registered                

        if len(courses_available) > 0:
            courses_not_already_done = []
            courses_not_already_done = remove_completed_by_student(request, courses_not_currently_registered)
            courses_available = courses_not_already_done

        if len(courses_available) > 0:
            courses_prereqs_met = []
            courses_prereqs_met = remove_prereqs_missing(request, courses_not_already_done)
            courses_available = courses_prereqs_met

    except Exception as e:
        courses_available = []

    return courses_available


# filters out courses already finished and passed from the given courses
def remove_completed_by_student(request, courses):
    not_completed_yet = []

    if (courses != None):
        try:
            for i in courses:
                if check_if_course_passed(request, i) == False:
                    not_completed_yet.append(i)

        except Exception as e:
            not_completed_yet = []

    return not_completed_yet


# returns all the prerequisites for the given courseid
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
# filters out courses whose prerequisities haven't been completed by the student
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


# helper function that evaluates if a course has been finisehd with passing grade
def check_if_course_passed(request, course):
    try:
        finished_course = Registered.objects.filter(cid=course.cid, studentid = Students.objects.get(email=request.user).sid, finished = True, type = 'lec')
        registered_course = Registered.objects.filter(cid=course.cid, studentid = Students.objects.get(email=request.user).sid, finished = False, type = 'lec')

        chosen_semester = request.session['semester']       
        chosen_year = int(request.session['year'])

        if len(finished_course) == 1 and finished_course[0].grade != '' and int(finished_course[0].grade) >= 50:
            return True

        if len(registered_course) == 1:
            if chosen_year > registered_course[0].year:
                return True

            if chosen_year == registered_course[0].year:
                if chosen_semester != registered_course[0].semester:
                    if chosen_semester == 'Summer' or (chosen_semester == 'Winter' and registered_course[0].semester == 'Fall'):
                        return True


    except Exception as e:
        return False
    return False

# filters out courses that the student is already registered for
def remove_currently_registered(request, courses):
    not_already_registered = []

    try:
        currently_registered = []
        currently_registered = Registered.objects.filter(studentid = Students.objects.get(email=request.user).sid, finished = False, type = 'lec')
        if len(currently_registered) >= 0:
            currently_registered_cids = get_cids(currently_registered)

            for i in courses:
                if i.cid.cid not in currently_registered_cids:
                    not_already_registered.append(i)

    except Exception as e:
        not_already_registered = []

    return not_already_registered

# filters out full courses
def remove_full_courses(request, courses):
    courses_with_capacity = []

    chosen_semester = request.session['semester']       
    chosen_year = int(request.session['year'])

    for i in courses:

        capacity = 0

        registered_courses = Registered.objects.filter(cid = i.cid, sectionid=i.sid, finished = False, semester=chosen_semester, year=chosen_year, type = i.type)

        if len(registered_courses) < i.capacity:
            courses_with_capacity.append(i)

    return courses_with_capacity

# returns cids from given courses
def get_cids(courses):
    cids_list = []
    for i in courses:
        cids_list.append(i.cid)
    return cids_list

# json serialization helper function (needed for javascript parsing)
def json_serialize(courses):
    #if (courses != None) and len(courses) > 0:
    return serializers.serialize('json',courses, use_natural_foreign_keys = True)
    #return []

# fetches the cache for specified key
# set with cache.set('key', 'cache_name')
def cached_queries(key):
    return {'cache': cache.get(key)}

