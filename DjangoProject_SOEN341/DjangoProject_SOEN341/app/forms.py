"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class ChangeEmailForm(forms.Form):
    new_email = forms.CharField(label='New Email Address', 
                                max_length=30, min_length=10, 
                                widget=forms.TextInput({
                                    'class': 'form-control', 
                                    'placeholder': 'Enter New Email'}))

    password_confirmation = forms.CharField(label=_("Password"),
                               max_length=30, min_length=4,
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm Password'}))

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=_("Old Password"),
                               max_length=30, min_length=4,
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Confirm Old Password'}))

    new_password = forms.CharField(label=_("New Password"),
                               max_length=30, min_length=4,
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'New Password'}))

    repeat_new_password = forms.CharField(label=_(""),
                                 max_length=30, min_length=4,
                                 widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Repeat New Password'}))
