
from django.urls import path
from . import  views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [

    path('',views.PeHome,name='PEHome'),
    path('dashboard', staff_member_required(views.dashboard), name='dashboard'),
    path('reports', staff_member_required(views.reports), name='reports'),
    path('Recommendation', staff_member_required(views.Matching), name='Matching'),
    path('term-of-use.html', views.termsofuse, name='termsofuse'),

]
