from django.urls import path

from . import  views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),

    path('error', views.register_error, name='error'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]