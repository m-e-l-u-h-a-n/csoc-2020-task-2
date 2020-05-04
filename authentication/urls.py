from django.urls import path,include
from authentication.views import *

urlpatterns = [
    path('login', loginView, name='Login'),
    path('signup', registerView, name='SignUp'),
    path('logout', logoutView, name='logout'),
]