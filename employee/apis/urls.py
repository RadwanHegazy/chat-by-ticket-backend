from django.urls import path
from .views import login, profile


urlpatterns = [
    path('',profile.ProfileView),
    path('login/',login.LoginView),
]