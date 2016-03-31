from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

addcourses = []
addsections = []

def workshop(request):
    """Renders the workshop page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        #addcourses = []
        classes = []
        studentID = Students.objects.get(email=request.user)
        finished = Registered.objects.filter(finished=1).filter(studentid=studentID)
        finish_exclude = [i.cid for i in finished]
        suggested_sequence = Sequence.objects.exclude(cid__in=finish_exclude).order_by('year', 'semester', 'cid').filter(year='1', semester='fall')

        if not request.POST.get('add'):
            if request.POST.get('addcourse') == '':
                pass
            else:
                addcourses.append(request.POST.get('addcourse'))
                addc = Courses.objects.filter(cid__in=addcourses)
                #addsections = Courses.objects.filter(cid__in=addcourses)
                for i in addcourses:
                    print i
                for j in addc:
                    addsections.append(j)
                    #print j.sid
        #if not request.POST.get('generate'):
        #    print 'clear list'
        #    del addcourses[:]
        for i in suggested_sequence:
            filteri = Courses.objects.filter(cid=i.cid, type='lec')
            for j in range(len(filteri)):
                cc = filteri[j]
                if Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='tut'):
                    tutlock = 0
                    tutorial = Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='tut')
                    for k in range(len(tutorial)):
                        for course in classes:
                            assigned = Courses.objects.get(id=course)
                            if tutorial[k].timeslot1.day == assigned.timeslot1.day or tutorial[k].timeslot1.day == assigned.timeslot2.day:
                                if tutorial[k].timeslot1.starthour >= assigned.timeslot1.endhour or tutorial[k].timeslot1.endhour <= assigned.timeslot2.starthour:
                                    #classes.append(tutorial[k].id)
                                    tutlock = k
                                else:
                                    tutlock = 0
                        classes.append(tutorial[tutlock].id)
                        tutlock = 1
                        break
                else:
                    tutlock = 1
                if Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='lab') and tutlock == 1:
                    lablock = 0
                    lab = Courses.objects.filter(sid__startswith=cc.sid, cid=cc.cid, type='lab')
                    for h in range(len(lab)):
                        for course2 in classes:
                            assigned2 = Courses.objects.get(id=course2)
                            if lab[h].timeslot1.day == assigned2.timeslot1.day or lab[h].timeslot1.day == assigned2.timeslot2.day:
                                if lab[h].timeslot1.starthour >= assigned2.timeslot1.endhour or lab[h].timeslot1.endhour <= assigned2.timeslot2.starthour:
                                    #classes.append(lab[h].id)
                                    lablock = h
                                else:
                                    lablock = 0
                        classes.append(lab[lablock].id)
                        lablock = 1
                        break
                else:
                    lablock = 1
                #classes.append(cc.id)
                if tutlock == 1 and lablock == 1:
                    classes.append(cc.id)
                    break
            suggested_sequence = Courses.objects.filter(id__in=classes)
    else:
        suggested_sequence = Courses.objects.order_by('year', 'semester', 'cid')
    if request.POST.get('gensched'):
        return render(request, 'schedule/schedule.html', context_instance = RequestContext(request, {'suggested_sequence': suggested_sequence}))
    return render(
        request,
        'workshop/workshop.html',
        context_instance = RequestContext(request,
        {
            'title':'Workshop',
            'suggested_sequence': suggested_sequence,
            'addcourses': addcourses,
            'addsections': addsections,
            #'constraints': '1',
            #'schedule': ,
            #'finished_courses': finished,
            #'prerequisites': Prerequisites.objects.all(),
            'message':'Your workshop page.',
            'year':datetime.now().year,
        })
    )
