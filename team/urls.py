from django.urls import path
from team.views import TeamAPI

urlpatterns = [
    path('', TeamAPI.as_view())

]