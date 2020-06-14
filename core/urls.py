from django.urls import path
from core.views import profileView, updateProfile, home

urlpatterns = [
    path('user/<str:username>', profileView, name="profile"),
    path('profile/update/', updateProfile, name="updateprofile"),
    path('home/', home, name="home")
]
