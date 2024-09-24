from django.urls import path
from authentication.views import UserRegistration, UserLogin

urlpatterns = [
    path('signup/', UserRegistration.as_view()),
    path('login/', UserLogin.as_view()),

]