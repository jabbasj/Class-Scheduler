from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from django.shortcuts import redirect

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

from datetime import time

def workshop(request):
    """Renders the workshop page."""
    assert isinstance(request, HttpRequest)

    if (request.user.is_authenticated()):
        return post_handler(request)

    return render(
        request,
        'workshop/workshop.html',
        context_instance = RequestContext(request,
        {
            'title':'Workshop',
            'message':'Your workshop page.',
            'year':datetime.now().year,
        })
    )


def post_handler(request):

    chosen_semester = None
    chosen_year = None
    student = None
    suggested_sequence = []     
    courses_available = []  
    

    chosen_semester, chosen_year, suggested_sequence = get_suggested_sequence(request)

    if chosen_semester != None and chosen_year != None:
        courses_available = get_sections_available_to_student(request)

    if 'generate' in request.POST.keys():
        return find_courses_within_constraints(request, suggested_sequence, courses_available)

    return render(
        request,
        'workshop/workshop.html',
        context_instance = RequestContext(request,
        {
            'title':'Workshop',
            'chosen_semester': chosen_semester,
            'chosen_year': chosen_year,
            'suggested_sequence': suggested_sequence,
            'courses_available': courses_available,
            'message':'Your workshop page.',
            'year':datetime.now().year,
        })
    )


# get the semester/year and sequence associated with it
def get_suggested_sequence(request):
    chosen_semester = None
    chosen_year = None
    student = None
    suggested_sequence = []

    if 'view' in request.POST.keys():
        chosen_semester = request.POST.get('semester')
        chosen_year = request.POST.get('year')
        request.session['year'] = chosen_year
        request.session['semester'] = chosen_semester

    elif 'semester' in request.session and 'year' in request.session: 
        chosen_semester = request.session['semester']            
        chosen_year = request.session['year']
        
    try:            
        suggested_sequence = get_sequence(chosen_semester, chosen_year)
        
    except Exception as e:            
        suggested_sequence = []

    return chosen_semester, chosen_year, suggested_sequence

# gets suggested sequence for a semester/year
def get_sequence(chosen_semester, chosen_year):
    suggested_sequence = []
    c_year = int(chosen_year) - 2016
    try:
        suggested_sequence = Sequence.objects.filter(semester = chosen_semester, year = c_year)

    except Exception as e:
        suggested_sequence = []

    return suggested_sequence



def find_courses_within_constraints(request, suggested_sequence, courses_available):
    chosen_semester = request.session['semester']            
    chosen_year = request.session['year']
    student = None
    success = False
    error = ""
    chosen_combos = []   
    lecs = []
    tuts = []
    labs = []

    courses_selected, days_of_week, types_of_class = get_constraints(request)

    try:

        for cid in courses_selected:
            lecs.extend(get_sections_available_to_student(request, 'lec', cid, False))
            tuts.extend(get_sections_available_to_student(request, 'tut', cid, False))
            labs.extend(get_sections_available_to_student(request, 'lab', cid, False))

        combos = []
        unique_lecture_cids = []
        unique_lectures = []

        for lecture in lecs:
            corresponding_tutorials = []
            corresponding_labs = []

            if checkDay(lecture.id, days_of_week) and checkType(lecture.id, types_of_class):
                has_lab = False
                has_tut = False

                for tut in tuts:                        
                    if tut.cid == lecture.cid and tut.sid.startswith(lecture.sid):
                        has_tut = True
                        if checkDay(tut.id, days_of_week) and checkType(tut.id, types_of_class):
                            corresponding_tutorials.append(tut)

                for lab in labs:                        
                    if lab.cid == lecture.cid and lab.sid.startswith(lecture.sid):
                        has_lab = True
                        if checkDay(lab.id, days_of_week) and checkType(lab.id, types_of_class):
                            corresponding_labs.append(lab)
                                
                if lecture.cid.cid not in unique_lecture_cids:
                    unique_lecture_cids.append(lecture.cid.cid)
                    unique_lectures.append({'lec_cid': lecture.cid.cid, 'has_tut': has_tut, 'has_lab': has_lab})      
            
            if (has_tut and len(corresponding_tutorials) == 0) or (has_lab and len(corresponding_labs) == 0):
                error = "Your constraints filtered out all the tutorials or labs of: " + lecture.cid.cid

            combo = {'lec':lecture,'tuts': corresponding_tutorials, 'labs': corresponding_labs}
            combos.append(combo)

        unique_packages_that_fit_current_schedule = split_into_unique_combos(request, combos, unique_lectures)

        chosen_combos = unique_packages_that_fit_current_schedule[0]

        conflicts = []

        for combo in chosen_combos:
            lec = combo.get('lec')
            lab = combo.get('lab')
            tut = combo.get('tut')
            if lec != None:
                if tut != None:
                    if lab != None:
                        success, conflicts, new_registries = check_conflicts_and_register_student_to(request, [lec], [lab], [tut])
                    else:
                        success, conflicts, new_registries = check_conflicts_and_register_student_to(request, [lec], [], [tut])
                else:
                   success, conflicts, new_registries = check_conflicts_and_register_student_to(request, [lec], [], [])

            if len(conflicts) > 0:
                error += " " + conflicts[0].cid.cid + " does not fit with current schedule!"

        if len(chosen_combos) > 0 and len(chosen_combos) < len(courses_selected):
            error = "Your constraints filtered out one of your chosen lectures!"


    except Exception as e:
            lecs = []
            tuts = []
            labs = []
            success = False

    if success:
        return redirect('schedule')

    if len(chosen_combos) == 0 and error == "":
        error = "Failed to build schedule, courses chosen cannot be fit together with your current constraints and schedule."

    return render(
            request,
            'workshop/workshop.html',
            context_instance = RequestContext(request,
            {
                'title':'Workshop',
                'chosen_semester': chosen_semester,
                'chosen_year': chosen_year,
                'error': error,
                'suggested_sequence': suggested_sequence,
                'courses_available':  courses_available,
                'message':'Your workshop page.',
                'year':datetime.now().year,
            })
        )


def filter_not_fitting_together(unique_packages_per_lecture, unique_lectures):
    which_fit = []

    num_of_courses = len(unique_packages_per_lecture)

    indexes = []
    for num in range(0,num_of_courses):
        indexes.append(0)
    index = num_of_courses - 1

    final_indexes = []
    for num in range(0,len(unique_packages_per_lecture)):
        final_indexes.append(len(unique_packages_per_lecture[num]))

    success = False

    while (index >= 0):
        packages_to_test = []

        for i in range(0,num_of_courses):
            packages_to_test.append(unique_packages_per_lecture[i][indexes[i]])

        indexes[index] += 1

        if indexes[index] == len(unique_packages_per_lecture[index]):
            indexes[index] = 0
            index -= 1

        if len(packages_to_test) == len(unique_packages_per_lecture):
            success = fits_together(packages_to_test)

            if success:
                which_fit.append(packages_to_test)

            packages_to_test = []

    return which_fit


def fits_together(packages):

    flatten_packages = []

    for item in packages:
        flatten_packages.append(item['lec'])
        if item.get('tut') != None:
            flatten_packages.append(item.get('tut'))

        if item.get('lab') != None:
            flatten_packages.append(item.get('lab'))

    for i in range(0,len(flatten_packages)):
        for j in range(0, len(flatten_packages)):
            if not isAvail([flatten_packages[i]], [flatten_packages[j]]):
                if flatten_packages[i].cid != flatten_packages[j].cid and flatten_packages[i].sid != flatten_packages[j].sid:
                    return False
    return True


def split_into_unique_combos(request, combos, unique_lectures):
    unique_combos_per_lecture = []
    unique_packages_that_fit_current_schedule = []
    success = False

    for lecture in unique_lectures:
        combos_for_this_lecture_with_unique_section = combos_with_cid(combos, lecture['lec_cid'])

        all_posibilities = split_combos_into_unique_section_packages(combos_for_this_lecture_with_unique_section)
        unique_combos_per_lecture.append(all_posibilities)

    unique_packages_that_fit_current_schedule = filter_against_current_schedule(request, unique_combos_per_lecture, unique_lectures)
    
    combos_that_fit_together = filter_not_fitting_together(unique_packages_that_fit_current_schedule, unique_lectures)

    return combos_that_fit_together



def split_combos_into_unique_section_packages(combos):
    unique_section_packages = []

    for combo in combos:
        packages = []

        lec = combo['lec']
        tuts = combo['tuts']
        labs = combo['labs']

        tut_index = len(tuts)
        lab_index = len(labs)
        num_of_combinations = lab_index * tut_index

        if (tut_index != 0):
            for i in range(0,tut_index):
                if (lab_index == 0):
                    packages.append({'lec': lec, 'tut': tuts[i]})
                for j in range(0,lab_index):
                    packages.append({'lec': lec, 'tut': tuts[i], 'lab': labs[j]})

        elif lab_index != 0:
            for k in range(0, lab_index):
                packages.append({'lec': lec, 'lab': labs[k]})

        elif tut_index == 0 and lab_index == 0:
            packages.append({'lec': lec})

        unique_section_packages.extend(packages)     

    return unique_section_packages


def combos_with_cid(combos, cid):
    c_combos = []
    for i in combos:
        if i['lec'].cid.cid == cid:
            c_combos.append(i)
    return c_combos


def filter_against_current_schedule(request, unique_combos_per_lecture, unique_lectures):

    sem, year, courses_registered = get_registered_courses(request)

    filtered_list = []

    for course in unique_combos_per_lecture:
        available = []

        for i in range(0,len(course)):

            if isAvail([course[i]['lec']], courses_registered) and isAvail([course[i].get('tut')], courses_registered) and isAvail([course[i].get('lab')], courses_registered):
                available.append(course[i])

        filtered_list.append(available)

    return filtered_list



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
                    conflicts.append(lec[0])
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


# function for fetching lectures, tutorials and labs available to register for chosen semester
# if type_chosen is specified it looks for specified type
# if u specify unique, it gets only unique course_id
# if course_id_specified is given then it looks for sections related to that course
# if section_id_specified is given then it looks for sections with the given id
def get_sections_available_to_student(request, type_chosen = 'lec', course_id_specified = None, unique = True, section_id_specified = None):
    chosen_semester = None
    chosen_year = None
    suggested_sequence = []
    courses_available = []
    unique_courses = []

    chosen_semester, chosen_year, suggested_sequence = get_suggested_sequence(request)

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


# computes time conflicts between given new_course and given 'registered' course list
def isAvail(new_course, registered):
    if len(new_course) > 0 and new_course[0] != None:
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
def check_if_course_passed(request, courseid):
    try:
        finished_course = Registered.objects.filter(cid=courseid, studentid = Students.objects.get(email=request.user).sid, finished = True, type = 'lec')
        registered_course = Registered.objects.filter(cid=courseid, studentid = Students.objects.get(email=request.user).sid, finished = False, type = 'lec')

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
        registered = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=int(chosen_year), finished = False)
            
        for reg in registered:                
            courses_registered.append(Courses.objects.get(cid=reg.cid, sid=reg.sectionid, type=reg.type)) #semester=chosen_semester, year=chosen_year
        
    except Exception as e:            
        courses_registered = []

    return chosen_semester, chosen_year, courses_registered


def get_constraints(request):
    added = request.POST.getlist('add')
    dow = request.POST.getlist('day')
    tc = request.POST.getlist('classes')
    return added, dow, tc

def checkType(course, tc):
    cc = Courses.objects.get(id=course)
    noon = time(12, 0, 0)
    evening = time(18, 0, 0)
    midnight = time(23, 59, 59)
    dayconstraint = None
    if cc.timeslot1.endhour <= noon:
        if cc.timeslot2.day != 0:
            if cc.timeslot2.endhour <= noon:
                dayconstraint = 'morning'
        else:
            dayconstraint = 'morning'
    elif cc.timeslot1.endhour <= evening:
        if cc.timeslot2.day != 0:
            if cc.timeslot2.endhour <= evening:
                dayconstraint = 'afternoon'
        else:
            dayconstraint = 'afternoon'
    elif cc.timeslot1.endhour <= midnight:
        if cc.timeslot2.day != 0:
            if cc.timeslot2.endhour <= midnight:
                dayconstraint = 'evening'
        else:
            dayconstraint = 'evening'
    for t in tc:
        if t == dayconstraint:
            return True
    return False

#   missing online
def checkDay(course, dow):
    cc = Courses.objects.get(id=course)

    dow = [int(k) for k in dow]
    for day in range(len(dow)):
        if cc.timeslot1.day == dow[day]:
            if cc.timeslot2.day != 0:
                for day2 in range(len(dow)):
                    if cc.timeslot2.day == dow[day2]:
                        return True
            else:
                return True
    return False


# returns cids from given courses
def get_cids(courses):
    cids_list = []
    for i in courses:
        cids_list.append(i.cid)
    return cids_list

def get_unique_cids(courses):
    unique_cids_list = []
    for i in courses:
        if i.cid not in unique_cids_list:
            unique_cids_list.append(i.cid)
    return unique_cids_list