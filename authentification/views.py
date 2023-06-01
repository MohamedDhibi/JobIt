from django.shortcuts import render

# Create your views here.
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from JobIt import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import generateToken
from six import text_type
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe


# Create your views here.


def home(request, *args, **kwargs):
    return render(request, 'acceuil/acceuil.html')


def signup(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        role_select = request.POST['role_select']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['confirmpwd']
        if User.objects.filter(username=username):
            messages.error(request, 'username already taken please try another.')
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, 'This email has an account.')
            return redirect('signup')
        if len(username) > 10:
            messages.error(request, 'Please the username must not be more than 10 character.')
            return redirect('signup')
        if len(username) < 5:
            messages.error(request, 'Please the username must be at leat 5 characters.')
            return redirect('signup')
        if not username.isalnum():
            messages.error(request, 'username must be alphanumeric')
            return redirect('signup')

        if password != confirmpwd:
            messages.error(request, 'The password did not match! ')
            return redirect('signup')
        else:
            if role_select == "student":

                myuser1 = User.objects.create_user(username, email, password)
                myuser1.first_name = firstname
                myuser1.last_name = lastname
                myuser1.is_active = False
                myuser1.save()
                my_admin_group = Group.objects.get_or_create(name='Student')
                my_admin_group[0].user_set.add(myuser1)
                messages.success(request,
                                 'Your account has been successfully created. we have sent you an email You must comfirm in order to activate your account.')

            elif role_select == 'Employability pole':
                 messages.error(request, 'You do not have permission to register as an Employability Pole')
                 return render(request, 'register_error.html')
            else:
                 messages.error(request, 'Invalid role specified')
                 return redirect('home')



       # send email when account has been created successfully
        subject = "Welcome to JobIT"
        message = "Welcome " + myuser1.first_name + " " + myuser1.last_name + "\n thank for chosing us.\n In order to login you need to comfirm your email account.\n thanks\n\n\n JobIt"

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser1.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # send the confirmation email
        current_site = get_current_site(request)
        email_suject = "confirm your email"
        messageConfirm = render_to_string("emailConfiguration.html", {
            'name': myuser1.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser1.pk)),
            'token': generateToken.make_token(myuser1)
        })

        email = EmailMessage(
            email_suject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [myuser1.email]
        )

        email.fail_silently = False
        email.send()
        return redirect('signin')
    return render(request, 'authentification/signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'acceuil/acceuil.html', {"firstname": firstname})
        elif my_user.is_active == False:
            messages.error(request, 'you have not confirm your  email do it, in order to activate your account')
            return redirect('signin')
        else:
            messages.error(request, 'bad authentification')
            return redirect('home')

    return render(request, 'authentification/signin.html')


def register_error(request):
    return render(request, 'register_error.html')


def signout(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home')

def is_PE(user):
    return user.groups.filter(name='Employability Pole').exists()
def is_student(user):
    return user.groups.filter(name='Student').exists()
def afterlogin(request):
    if is_PE(request.user):
        return redirect('PEHome')
    elif is_student(request.user):
        return redirect('etudiantHome')
    else:
        return render(request,'Recommendation/index.html')
    return HttpResponse("home")


def activate(request, uidb64, token):
    try:
        uid = text_type(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active = True
        my_user.save()
        messages.success(request, "You are account is activated you can login by filling the form below.")
        return redirect("signin")
    else:
        messages.success(request, 'Activation failed please try again')
        return redirect('home')

