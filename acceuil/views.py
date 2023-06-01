from django.shortcuts import render

import JobIt.settings
# Create your views here.
def home(request):
    return render(request, 'acceuil/acceuil.html')

def aboutus(request):
    return render(request, 'acceuil/about-us.html')
def contactus(request):
    return render(request, 'acceuil/contactus.html')

import os
import uuid
from django.http import HttpResponse

def upload_complaints(request):
    if request.method == 'POST':
        complaint_text = request.POST.get('complaint_text', '')
        
        # Create the 'complaints' folder if it doesn't exist
        folder_path = os.path.join(os.getcwd(), 'complaints')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Generate a unique filename for the text file
        file_name = f"complaint_{uuid.uuid4()}.txt"
        
        # Construct the file path
        file_path = os.path.join(folder_path, file_name)
        
        # Write the complaint text to the file
        with open(file_path, 'w') as file:
            file.write(complaint_text)
        
        return render(request, 'acceuil/acceuil.html')

    return render(request, 'acceuil/contactus.html')
