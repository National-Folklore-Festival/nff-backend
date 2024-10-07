from rest_framework import serializers
from .models import Team, Member
from midtrans.serializers import TransactionSerializers


class MemberSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team')
    class Meta:
        model = Member
        fields = ['id', 'position', 'full_name', 'phone_number', 'team_id']

class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Member
        fields = ['position', 'full_name', 'phone_number']

class TeamSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializers(read_only=True)
    class Meta:
        model = Team
        fields = ['id', 'team_name', 'institution', 'location', 'phone_number', 'coach', 'main_category', 'sub_category', 'is_paid', 'transaction']
    
class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name', 'institution', 'location', 'phone_number','coach']