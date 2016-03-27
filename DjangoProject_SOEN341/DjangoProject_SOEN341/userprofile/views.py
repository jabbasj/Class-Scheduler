from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Students, Sequence, Registered, Courses, Prerequisites, Timeslots, AuthUser

from app.forms import ChangeEmailForm, ChangePasswordForm

def profile(request):
    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    student = None
    if (request.user.is_authenticated()):
        student = Students.objects.get(email=request.user)

    if request.method == 'POST':
        return post_handler(request)

    else:
        return render(
            request,
            'userprofile/profile.html',
            context_instance = RequestContext(request,
            {
                'title':'Profile',
                'student': student,
                'date':datetime.now(),
                'year':datetime.now().year,
                'change_email_form': ChangeEmailForm(),
                'change_password_form': ChangePasswordForm()
            })
        )

def post_handler(request):

    form = ChangeEmailForm(request.POST)
    pwd_change_success = False
    email_change_success = False
    student = None

    if form.is_valid():
        email_change_success = change_email(request)
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            pwd_change_success = change_password(request)

    if (request.user.is_authenticated()):
        student = Students.objects.get(email=request.user)

    return render(
            request,
            'userprofile/profile.html',
            context_instance = RequestContext(request,
            {
                'title':'Profile',
                'student': student,
                'date':datetime.now(),
                'year':datetime.now().year,
                'change_email_form': ChangeEmailForm(),
                'change_password_form': ChangePasswordForm(),
                'pwd_change_success': pwd_change_success,
                'email_change_success': email_change_success
            }))

def change_email(request):
    form = ChangeEmailForm(request.POST)
    if form.is_valid():
        student = Students.objects.get(email=request.user)
        user = AuthUser.objects.get(username=request.user)

        if request.user.check_password(form.cleaned_data['password_confirmation']):
            student.email = form.cleaned_data['new_email']
            user.username = form.cleaned_data['new_email'] #email used as username
            user.email = form.cleaned_data['new_email']
            request.user.username = form.cleaned_data['new_email']

            request.user.save()
            student.save()
            user.save()
            return True

    return False

def change_password(request):
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        student = Students.objects.get(email=request.user)
        user = AuthUser.objects.get(username=request.user)

        if request.user.check_password(form.cleaned_data['old_password']) and form.cleaned_data['new_password'] == form.cleaned_data['repeat_new_password']:
            student.password = form.cleaned_data['new_password'] #not really needed                       
            request.user.set_password(form.cleaned_data['new_password'])

            request.user.save()        
            student.save()
            return True

    return False

