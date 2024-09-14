from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from .serializers import TeamSerializer, MemberSerializer
from .models import Team, Member


class TeamResponse(serializers.Serializer):
    message = serializers.CharField()
    data = TeamSerializer()


class TeamAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        team_data = TeamSerializer(data = request.data)

        if team_data.is_valid():
            new_team = Team.objects.create(
                team_name = team_data.validated_data['team_name'],
                institution = team_data.validated_data['institution'],
                location = team_data.validated_data['location'],
                phone_number = team_data.validated_data['phone_number'],
                coach = team_data.validated_data['coach'],
                main_category = team_data.validated_data['main_category'],
                sub_category = team_data.validated_data['sub_category'],
                owner = request.user
            )
            new_team.save()

            team_serializer = TeamSerializer(new_team)

            serializer = TeamResponse(
                data = { 
                    'message': "Team created",
                    'data': team_serializer.data
                }
            )
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(team_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(Self,request):

        return Response()

class TeamMemberAPI(APIView):
    def post():

        return Response()
    