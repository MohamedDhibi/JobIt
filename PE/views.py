

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def Matching(request):
    return render(request, 'PE/Matching.html')

# Function to check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# View that requires admin login
@login_required
@user_passes_test(is_admin)
def PeHome(request):
    return render(request, 'PE/PEHome.html')
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'PE/dashboard.html')
import os

@login_required
@user_passes_test(is_admin)
def reports(request):
    folder_path = os.path.join(os.getcwd(), 'complaints')
    
    # Get the list of files in the folder
    files = os.listdir(folder_path)
    
    # List to store the contents of the text files
    complaints = []
    
    # Read the contents of each text file
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                complaint_text = file.read()
                complaints.append(complaint_text)
    
    # Pass the list of complaints to the template
    context = {
        'complaints': complaints
    }
    
    return render(request, 'PE/reports.html',context )

@login_required
@user_passes_test(is_admin)
def termsofuse(request):
    return render(request, 'PE/terms-of-use.html')



