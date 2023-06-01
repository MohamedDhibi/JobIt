
from django.urls import path
from . import  views
urlpatterns = [

    path('',views.home,name='home'),
    path('about-us.html',views.aboutus,name='About-us'),
    path('contact-us',views.contactus,name='Contact-Us'),
    path('upload_complaints',views.upload_complaints,name='upload_complaints'),
]
