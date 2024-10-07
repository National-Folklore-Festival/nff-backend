from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, status
from .serializers import TeamSerializer, TeamUpdateSerializer, MemberSerializer, MemberUpdateSerializer
from .models import Team, Member
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404


class TeamResponse(serializers.Serializer):
    message = serializers.CharField()
    data = TeamSerializer()

class TeamAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        new_team = serializer.save(owner=request.user)
            
        return Response({
            'message': "Team created",
            'data': TeamSerializer(new_team).data
        }, status=status.HTTP_201_CREATED)
         
    def get(self,request):
        teams = Team.objects.filter(owner=request.user).prefetch_related(
            Prefetch('members', queryset=Member.objects.filter(is_valid=True)))

        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class TeamDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, team_id=None):
        team  = get_object_or_404(Team, pk=team_id)

        if request.user != team.owner:
            return Response({"message": "Not authorized to access this team"}, 
                            status=status.HTTP_403_FORBIDDEN)
            
        serializer = TeamSerializer(team)
        return Response(serializer.data)
   
    def put(Self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)

        if request.user != team.owner:
            return Response({"message": "Not authorized to access this team"}, 
                            status=status.HTTP_403_FORBIDDEN)

        serializer = TeamUpdateSerializer(team, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
                'message': "Team updated",
                'data': TeamSerializer(team).data})
    
    def delete(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)

        if request.user != team.owner:
            return Response({"message": "Not authorized to access this team"}, 
                            status=status.HTTP_403_FORBIDDEN)

        team.delete()
        
        return Response({"message": f"Team {team.team_name} has been deleted"}, 
                        status=status.HTTP_200_OK)
    

class MemberResponse(serializers.Serializer):
    message = serializers.CharField()
    data = MemberSerializer()

class MemberAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MemberSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        team_object = serializer.validated_data['team']
        
        if request.user != team_object.owner:
            return Response({"message": "Not authorized to add members to this team"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        new_member = serializer.save()

        return Response({
            'message': "Member created",
            'data': MemberSerializer(new_member).data
        }, status=status.HTTP_201_CREATED)
    
    def get(self, request): #from any teams owned by user
        teams = Team.objects.filter(owner=request.user)
        members = Member.objects.filter(team__in=teams)
        serializer = MemberSerializer(members, many=True)

        return Response(serializer.data)

class MemberDetailAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def get(self, request, member_id): #specific member 
        member = get_object_or_404(Member, pk=member_id)

        if(request.user != member.team.owner):
            return Response({"message": "Not authorized to access this member"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = MemberSerializer(member) 
        return Response(serializer.data)
    
    def put(self, request, member_id):
        member = get_object_or_404(Member, pk=member_id)
        
        if request.user != member.team.owner:
            return Response({"message": "Not authorized to update this member"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        member_data = MemberUpdateSerializer(member, data=request.data)
        member_data.is_valid(raise_exception=True)
        member_data.save()

        return Response({
                'message': "Member updated",
                'data': MemberSerializer(member).data})
    
    def delete(self, request, member_id):
        member = get_object_or_404(Member, pk=member_id)

        if request.user != member.team.owner:
            return Response({"message": "Not authorized to delete this member"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        member.delete()

        return Response({"message": f"Member {member.full_name} has been deleted"})

