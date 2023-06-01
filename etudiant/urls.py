
from django.urls import path
from . import  views
urlpatterns = [

    path('etudiant2',views.resume,name='resume'),
    path('etudiant1', views.etudiantHome, name='etudiantHome'),
    path('uploadedResumes', views.UploadedResumes, name='uploadedResumes'),
]
