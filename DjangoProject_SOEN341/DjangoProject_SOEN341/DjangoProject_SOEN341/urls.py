"""
Definition of urls for DjangoProject_SOEN341.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm


from home.views import home
#from app.views import contact
#from app.views import about
from userprofile.views import profile
from record.views import record
from schedule.views import schedule
from workshop.views import workshop

from django.contrib.auth.views import login
from django.contrib.auth.views import logout

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^profile', profile, name='profile'),
    url(r'^record', record, name='record'),
    url(r'^workshop', workshop, name='workshop'),
    url(r'^schedule', schedule, name='schedule'),
    #url(r'^contact$', contact, name='contact'),
    #url(r'^about', about, name='about'),
    url(r'^login/$',
        login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include(admindocs_urls)),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
