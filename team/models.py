import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

'''
class MainCategory(models.TextChoices):
    PADUS = "PADUS", _("PADUS")
    TATRA = "TATRA", _("TATRA")

class PadusCategory(models.TextChoices):
    PADUS_A = "PADUS_A", _("PADUS_A")
    PADUS_B = "PADUS_B", _("PADUS_B")

class TatraCategory(models.TextChoices):
    TATRA_A = "TATRA_A", _("TATRA_A")
    TATRA_B = "TATRA_B", _("TATRA_B")
    TATRA_C = "TATRA_C", _("TATRA_C")
'''

class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team_name = models.CharField(unique=True, max_length=100)
    institution = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    coach = models.CharField(max_length=30)
    main_category = models.CharField(max_length=30) #skip choices?
    sub_category = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name


class Member(models.Model):
    full_name = models.CharField(max_length=1024)
    dob = models.DateTimeField()
    phone_number = models.CharField(max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.full_name} - {self.team.team_name}'
