from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from django.core import serializers

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

added_courses = []
solutions = []

def workshop(request):
    """Renders the workshop page."""
    assert isinstance(request, HttpRequest)
    if (request.user.is_authenticated()):
        classes = []
        studentID = Students.objects.get(email=request.user)
        finished = Registered.objects.filter(finished=1).filter(studentid=studentID)
        finish_exclude = [i.cid for i in finished]
        suggested_sequence = Sequence.objects.exclude(cid__in=finish_exclude).order_by('year', 'semester', 'cid').filter(year='1', semester='fall')
        #for i in range(len(suggested_sequence))[0:]:
        #    print i

        # Get semester and year
        if request.method == 'POST':
            semester, year = semester_select(request)
            #print semester
            #print year
            if semester != None:
                sem = semester.lower()
                suggested_sequence = Sequence.objects.exclude(cid__in=finish_exclude).order_by('year', 'semester', 'cid').filter(year='1', semester=sem)
        else:
            semester = None
            year = None

        # Get constraints
        if request.POST.get('constraints'):
            added, dayofweek, courses, location = constraints(request)
            added2 = Sequence.objects.filter(cid__in=added).filter(semester='winter', year='1')
            solutions2 = solve(request, 0, added2, classes)
            semester = 'winter'
            year = '2016'
            #return solve(request, 0, added2, classes)
            for i in solutions2:
                print i
            suggested_sequence2 = Courses.objects.filter(id__in=solutions2)
            for i in suggested_sequence2:
                print i
                print "%s - %s" % (i.timeslot1.starthour, i.timeslot1.endhour)
            #for j in suggested_sequence2:
            #    Registered.create(studentID, j.cid.cid, j.sid, semester, year, j.type, '', False )
            request.session['year'] = '2016'
            request.session['semester'] = 'winter'
            return render(request, 'schedule/schedule.html', context_instance = RequestContext(request, {'json_courses_registered': serializers.serialize('json', suggested_sequence2, use_natural_foreign_keys = True),}))

        return render(
            request,
            'workshop/workshop.html',
            context_instance = RequestContext(request,
            {
                'title':'Workshop',
                'suggested_sequence': suggested_sequence,
                'semester': semester,
                'year': year,
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
    cl = request.POST.getlist('classes')
    loc = request.POST.getlist('location')
    return added, dow, cl, loc

def semester_select(request):
    chosen_semester = None
    chosen_year = None
    student = None
    if 'view' in request.POST.keys():
        chosen_semester = request.POST.get('semester')
        chosen_year = request.POST.get('year')
        try:
            student = Students.objects.get(email=request.user)
            registered = Registered.objects.filter(studentid=student.sid, semester=chosen_semester, year=chosen_year, finished = False)

            for reg in registered:
                courses_registered.append(Courses.objects.get(cid=reg.cid, sid=reg.sectionid, semester=chosen_semester, year=chosen_year, type=reg.type))

        except Exception as e:
            courses_registered = None
            courses_pending_confirmation = None
    return chosen_semester, chosen_year

def solve(request, course, suggested_sequence, classes):
    #print "just recursed"
    print "course = %d, size = %d" % (course, len(suggested_sequence))
    endlock = 0
    #solutions = []
    if course == len(suggested_sequence):
        #print "how did i get here?"
        del solutions[:]
        solutions.extend(classes)
        endlock = 1
        #suggested_sequence = Courses.objects.filter(id__in=solutions)
        for i in solutions:
            print i
        #suggested_sequence2 = Courses.objects.filter(id__in=solutions)
        #return render(request, 'schedule/schedule.html', context_instance = RequestContext(request, {'json_courses_registered': serializers.serialize('json', suggested_sequence2, use_natural_foreign_keys = True),}))
        return solutions
    else:
        #print "else %d" % (course)
        #for i in range(len(suggested_sequence))[course:]:
            #print suggested_sequence[i]
        filteri = Courses.objects.filter(cid=suggested_sequence[course].cid, type='lec')
        for j in range(len(filteri)):
            cc = filteri[j]
            #for op in filteri:
            #    print op.sid
            if Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='tut'):
                tutorial = Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='tut')
                if Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='lab'):
                    lab = Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='lab')
                    for k in range(len(tutorial)):
                        for l in range(len(lab)):
                            if isAvail(lab[l].id, classes):
                            #if course >= 0:
                                #print "Lab is available"
                                if isAvail(tutorial[k].id, classes):
                                    #print "Tutorial is available"
                                #if course >= 0:
                                    if isAvail(cc.id, classes):
                                        #print "Lecture is available"
                                    #if course >= 0:
                                        #print "Lec = %s, Tut = %s, Lab = %s" % (cc, tutorial[k], lab[l])
                                        classes.append(cc.id)
                                        classes.append(tutorial[k].id)
                                        classes.append(lab[l].id)
                                        print "%s: %s - %s - %s section appended" % (cc.cid.cid, cc.sid, tutorial[k].sid, lab[l].sid)
                                        solve(request, course+1, suggested_sequence, classes)
                                        if endlock == 1:
                                            return solutions
                                        classes.remove(cc.id)
                                        classes.remove(tutorial[k].id)
                                        classes.remove(lab[l].id)
                                        print "%s: %s - %s - %s section removed" % (cc.cid.cid, cc.sid, tutorial[k].sid, lab[l].sid)
                else:
                    for k in range(len(tutorial)):
                        #if course >= 0:
                        if isAvail(tutorial[k].id, classes):
                            #print "Tutorial is available"
                            #if course >= 0:
                            if isAvail(cc.id, classes):
                                #print "Lecture is available"
                                #print "Lec = %s, Tut = %s" % (cc, tutorial[k])
                                classes.append(cc.id)
                                classes.append(tutorial[k].id)
                                print "%s: %s - %s section appended" % (cc.cid.cid, cc.sid, tutorial[k].sid)
                                solve(request, course+1, suggested_sequence, classes)
                                if endlock == 1:
                                    return solutions
                                classes.remove(cc.id)
                                classes.remove(tutorial[k].id)
                                print "%s: %s - %s section removed" % (cc.cid.cid, cc.sid, tutorial[k].sid)
            else:
                #if course >= 0:
                if isAvail(cc.id, classes):
                    #print "Lecture is available"
                    #print "Lec = %s" % (cc)
                    classes.append(cc.id)
                    print "%s - %s section appended" % (cc.cid.cid, cc.sid)
                    #print cc.cid
                    solve(request, course+1, suggested_sequence, classes)
                    if endlock == 1:
                        return solutions
                    classes.remove(cc.id)
                    print "%s - %s section removed" % (cc.cid.cid, cc.sid)
        print "classes"
        return solutions
        #suggested_sequence = Courses.objects.filter(id__in=solutions)
        #return render(request, 'schedule/schedule.html', context_instance = RequestContext(request, {'json_courses_registered': serializers.serialize('json',suggested_sequence, use_natural_foreign_keys = True),}))
    #suggested_sequence = Courses.objects.filter(id__in=solutions)
    #return render(request, 'schedule/schedule.html', context_instance = RequestContext(request, {'json_courses_registered': serializers.serialize('json',suggested_sequence, use_natural_foreign_keys = True),}))

def isAvail(course, classes):
    cc = Courses.objects.get(id=course)
    if cc.timeslot1.day == 0:
        return True
    for i in classes:
        assigned = Courses.objects.get(id=i)
        if cc.timeslot1.day == assigned.timeslot1.day or cc.timeslot1.day == assigned.timeslot2.day:
            if cc.timeslot1.starthour == assigned.timeslot1.starthour or cc.timeslot1.endhour == assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot1.starthour <= cc.timeslot1.starthour and cc.timeslot1.starthour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot1.starthour and cc.timeslot1.starthour <= assigned.timeslot2.endhour:
                return False
            elif assigned.timeslot1.starthour <= cc.timeslot2.starthour and cc.timeslot2.starthour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot2.starthour and cc.timeslot2.starthour <= assigned.timeslot2.endhour:
                return False

            elif assigned.timeslot1.starthour <= cc.timeslot1.endhour and cc.timeslot1.endhour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot1.endhour and cc.timeslot1.endhour <= assigned.timeslot2.endhour:
                return False
            elif assigned.timeslot1.starthour <= cc.timeslot2.endhour and cc.timeslot2.endhour <= assigned.timeslot1.endhour:
                return False
            elif assigned.timeslot2.starthour <= cc.timeslot2.endhour and cc.timeslot2.endhour <= assigned.timeslot2.endhour:
                return False
    #print "TRUE"
    return True
