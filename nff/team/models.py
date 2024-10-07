import uuid
from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team_name = models.CharField(unique=True, max_length=100)
    institution = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    coach = models.CharField(max_length=30)
    main_category = models.CharField(max_length=30) 
    sub_category = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return self.team_name


class Member(models.Model):
    full_name = models.CharField(max_length=1024)
    phone_number = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    is_valid = models.BooleanField(default=False)
    position = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.full_name} - {self.team.team_name}'
