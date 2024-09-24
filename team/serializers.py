from rest_framework import serializers


class MemberSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    full_name = serializers.CharField()
    dob = serializers.DateTimeField()
    phone_number = serializers.CharField()
    team_id = serializers.UUIDField()

class TeamSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    team_name = serializers.CharField()
    institution = serializers.CharField()
    location = serializers.CharField()
    phone_number = serializers.CharField()
    coach = serializers.CharField()
    main_category = serializers.CharField()
    sub_category = serializers.CharField()
    members = MemberSerializer(many=True, required=False)