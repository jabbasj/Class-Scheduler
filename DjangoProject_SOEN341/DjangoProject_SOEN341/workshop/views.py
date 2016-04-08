from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from django.shortcuts import redirect

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

from datetime import time

#solutions = []
solution2 = []

def workshop(request):
    """Renders the workshop page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated() and not request.user.is_staff:
        solutions = []
        classes = []
        error = None
        studentID = Students.objects.get(email=request.user)
        finished = Registered.objects.filter(finished=1, studentid=studentID)
        registered = Registered.objects.filter(finished=0, studentid=studentID)
        finish_exclude = [i.cid for i in finished]
        registered_exclude = [j.cid for j in registered]
        combined = []
        combined.extend(finish_exclude)
        combined.extend(registered_exclude)
        listofreq = excludePrereq(request, studentID)
        combined.extend(listofreq)
        suggested_sequence = Sequence.objects.exclude(cid__in=combined).filter(year='0', semester='fall')
        # Get semester and year
        if request.method == 'POST':
            chosen_semester, chosen_year = semester_select(request)
            if chosen_semester != None and chosen_year != None:
                suggested_sequence = Sequence.objects.exclude(cid__in=combined).order_by('year', 'cid')
            else:
                error = 'Please select both a semester and a year.'
        else:
            chosen_semester = None
            chosen_year = None

        # Get constraints
        if request.POST.get('constraints'):
            chosen_semester = request.session['semester']
            chosen_year = request.session['year']
            reg = Registered.objects.filter(finished=0, studentid=studentID, semester=chosen_semester, year=chosen_year)
            for k in reg:
                classes.append(Courses.objects.get(cid=k.cid, sid=k.sectionid).id)
            classes2 = []
            classes2.extend(classes)
            added, dayofweek, typeclass = constraints(request)
            if not added:
                error = 'No courses were selected. Please select one or more courses.'
                #return render(request, 'workshop/workshop.html', context_instance = RequestContext(request,{'title':'Workshop', 'error': error, 'year':datetime.now().year,}))
            added2 = Sequence.objects.filter(cid__in=added)
            solutions2 = solve(request, 0, added2, classes, dayofweek, typeclass, solutions)
            if not solutions2:
                if classes2:
                    error = 'No possible combinations due to conflicts from previously registered courses. Please unregister and try again!'
                else:
                    error = 'No possible schedule combinations could be generated. Please include less constraints and try again!'
            else:
                suggested_sequence2 = Courses.objects.filter(id__in=solutions2)
                del solutions
                del solutions2
                for j in suggested_sequence2:
                    Registered.create(studentID, j.cid.cid, j.sid, chosen_semester, chosen_year, j.type, '', False )
                return redirect('schedule')
                #return render(request, 'schedule/schedule.html', context_instance = RequestContext(request, {'json_courses_registered': serializers.serialize('json', suggested_sequence2, use_natural_foreign_keys = True),}))

        return render(
            request,
            'workshop/workshop.html',
            context_instance = RequestContext(request,
            {
                'title':'Workshop',
                'suggested_sequence': suggested_sequence,
                'chosen_semester': chosen_semester,
                'chosen_year': chosen_year,
                'error': error,
                'message':'Your workshop page.',
                'year':datetime.now().year,
            })
        )

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

def constraints(request):
    added = request.POST.getlist('add')
    dow = request.POST.getlist('day')
    tc = request.POST.getlist('classes')
    return added, dow, tc

def semester_select(request):
    chosen_semester = None
    chosen_year = None
    if 'view' in request.POST.keys():
        chosen_semester = request.POST.get('semester')
        chosen_year = request.POST.get('year')
        request.session['year'] = chosen_year
        request.session['semester'] = chosen_semester
    return chosen_semester, chosen_year

def solve(request, course, suggested_sequence, classes, dow, tc, solutions):
    if course == suggested_sequence.count():
        #del solutions[:]
        solutions.extend(classes)
        return solutions
    else:
        filteri = Courses.objects.filter(cid=suggested_sequence[course].cid, type='lec')
        for j in range(filteri.count()):
            cc = filteri[j]
            if Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='tut'):
                tutorial = Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='tut')
                if Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='lab'):
                    lab = Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='lab')
                    for k in range(tutorial.count()):
                        for l in range(lab.count()):
                            if isAvail(lab[l].id, classes, dow, tc):
                                if isAvail(tutorial[k].id, classes, dow, tc):
                                    if isAvail(cc.id, classes, dow, tc):
                                        classes.append(cc.id)
                                        classes.append(tutorial[k].id)
                                        classes.append(lab[l].id)
                                        solve(request, course+1, suggested_sequence, classes, dow, tc, solutions)
                                        if solutions:
                                            break
                                        classes.remove(cc.id)
                                        classes.remove(tutorial[k].id)
                                        classes.remove(lab[l].id)
                else:
                    for k in range(tutorial.count()):
                        if isAvail(tutorial[k].id, classes, dow, tc):
                            if isAvail(cc.id, classes, dow, tc):
                                classes.append(cc.id)
                                classes.append(tutorial[k].id)
                                solve(request, course+1, suggested_sequence, classes, dow, tc, solutions)
                                if solutions:
                                    break
                                classes.remove(cc.id)
                                classes.remove(tutorial[k].id)
            else:
                if isAvail(cc.id, classes, dow, tc):
                    classes.append(cc.id)
                    solve(request, course+1, suggested_sequence, classes, dow, tc, solutions)
                    if solutions:
                        break
                    classes.remove(cc.id)
        return solutions
    #return solutions

def isAvail(course, classes, dow, tc):
    cc = Courses.objects.get(id=course)
    if cc.timeslot1.day == 0:
        return True
    for i in classes:
        assigned = Courses.objects.get(id=i)
        if cc.timeslot1.day == assigned.timeslot1.day or cc.timeslot1.day == assigned.timeslot2.day:
            if cc.timeslot1.starthour == assigned.timeslot1.starthour or cc.timeslot1.endhour == assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot1.starthour <= cc.timeslot1.starthour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot1.starthour <= assigned.timeslot2.endhour:
                return False
            elif assigned.timeslot1.starthour <= cc.timeslot2.starthour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot2.starthour <= assigned.timeslot2.endhour:
                return False

            elif assigned.timeslot1.starthour <= cc.timeslot1.endhour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot1.endhour <= assigned.timeslot2.endhour:
                return False
            elif assigned.timeslot1.starthour <= cc.timeslot2.endhour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot2.endhour <= assigned.timeslot2.endhour:
                return False
    if checkDay(course, dow) and checkType(course, tc):
        return True
    else:
        return False
    return True

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

def checkPrereq(request, course):
    prerequisite_classes = []

    if len(prerequisite_classes) == 0:
        first = Prerequisites.objects.filter(pid=course)
        for k in first:
            prerequisite_classes.append(k.rid)

    for i in prerequisite_classes:
        potentially_new = Prerequisites.objects.filter(pid=i)
        for j in potentially_new:
            if j not in prerequisite_classes:
                prerequisite_classes.append(j.rid)
    return prerequisite_classes

def excludePrereq(request, student):
    prereq = Sequence.objects.all()
    listofreq = []
    for i in prereq:
        if Prerequisites.objects.filter(pid=i.cid):
            for j in Prerequisites.objects.filter(pid=i.cid):
                if Registered.objects.filter(studentid=student, cid=j.rid):
                    continue
                else:
                    listofreq.append(i.cid)
    return listofreq
