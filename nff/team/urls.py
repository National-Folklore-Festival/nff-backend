from django.urls import path
from team.views import TeamAPI, TeamDetailAPI, MemberAPI, MemberDetailAPI

urlpatterns = [
    path('', TeamAPI.as_view()),
    path('<uuid:team_id>/', TeamDetailAPI.as_view()),
    path('member/', MemberAPI.as_view()),
    path('member/<int:member_id>/', MemberDetailAPI.as_view())
]