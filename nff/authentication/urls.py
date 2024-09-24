from django.urls import path
from authentication.views import UserRegistration, UserLogin, UserLogout

urlpatterns = [
    path('signup/', UserRegistration.as_view()),
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view())
]