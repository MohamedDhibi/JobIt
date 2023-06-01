from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect

import authentification.views
from etudiant.models import *
from etudiant.forms import *
from . import  views
from authentification import views

from django.contrib.auth.decorators import login_required,user_passes_test

from django.shortcuts import render
import pythoncom
pythoncom.CoInitialize()
import comtypes.client
# Create your views here.

# Create your views here.
def uploaded_offers_view(request):
    if request.method == 'POST':
        # Handle the file upload logic here
        file = request.FILES.get('file')
        if file is not None:
            # Process the uploaded file
            # For example, you can save the file to the 'uploadedOffers' folder
            with open('uploadedOffers/' + file.name, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Optionally, you can perform additional operations with the uploaded file
            
            # Redirect to a success page or render a template
            return render(request, 'PE/uploadoffersuccess.html')
        else:
        # Render the upload form
            return render(request, 'PE/uploadoffer.html')
        

def uploadoffer(request):
    return render(request, 'PE/uploadoffer.html')