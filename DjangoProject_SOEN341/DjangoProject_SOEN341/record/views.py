from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus.flowables import PageBreak

def record(request):
    """Renders the academic record page."""
    assert isinstance(request, HttpRequest)
    completed_courses = None

    if request.method == 'POST':
        return generate_and_download_pdf(request)

    if (request.user.is_authenticated()):
        completed_courses = Registered.objects.filter(studentid = Students.objects.get(email=request.user).sid, finished = True)

    return render(
        request,
        'record/records.html',
        context_instance = RequestContext(request,
        {
            'title':'Academic Record',
            'completed_courses': completed_courses,
            'year':datetime.now().year,
        })
    )


def generate_and_download_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="unofficial_transcript.pdf"'
    buffer = BytesIO()

    student = Students.objects.get(email=request.user)
    completed_courses = Registered.objects.filter(studentid = Students.objects.get(email=request.user).sid, finished = True)
    currently_registered_courses = Registered.objects.filter(studentid = Students.objects.get(email=request.user).sid, finished = False)

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
 
    p.drawString(30,750,'CONCORDIA UNIVERSITY')
    p.drawString(30,735,'UNOFFICIAL TRANSCRIPT')
    p.drawString(420,735,'Valid as of: ' + datetime.now().strftime("%Y-%m-%d"))
    p.line(30,732,580,732)

    first_line = 650
    jump_line = 20

    p.drawString(30,first_line,'Student Name:')
    p.drawString(120,first_line,student.lastname + ', ' + student.firstname)
    p.line(30,first_line - 3,300,first_line - 3)

    p.drawString(30, first_line - jump_line, 'Student ID:')
    p.drawString(120, first_line - jump_line, str(student.sid))
    p.line(30,first_line - jump_line - 3, 300, first_line - jump_line - 3)

    p.drawString(30, first_line - 2 * jump_line, 'E-mail:')
    p.drawString(120, first_line - 2 * jump_line, student.email)
    p.line(30,first_line - 2 * jump_line - 3, 300, first_line - 2 * jump_line - 3)

    line_jumps = 4

    p.drawString(30, first_line - 3 * jump_line, 'Finished Courses:')
    #p.line(30, first_line - 3 * jump_line - 3 , 300,first_line - 3 * jump_line -3)

    for finished_class in completed_courses:
        if finished_class.type == 'lec':
            p.drawString(120, first_line - line_jumps * jump_line, finished_class.cid + '  -  ' + finished_class.semester + ', ' + str(finished_class.year) + ' -   Grade:  ' + finished_class.grade)
            line_jumps += 1
            if line_jumps == 30:                
                p.showPage()
                line_jumps = 1
                first_line = 750
    
    p.line(30, first_line - line_jumps * jump_line - 3, 300, first_line - line_jumps * jump_line - 3)
    
    # do we need to add "registered (unfinished)" courses?

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response