from django.db import models
import uuid

# Create your models here.
class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team = models.OneToOneField('team.Team', on_delete=models.CASCADE, related_name='transaction')
    transaction_id = models.CharField(max_length=100, editable=False, unique=True)
    midtrans_token = models.CharField(max_length=100, editable=False, unique=True)
    redirect_url = models.URLField(editable=False, null=True, blank=True)
    
    gross_amount = models.IntegerField()

    payment_status = models.CharField(max_length=100, default="pending")
    fraud_status = models.CharField(max_length=100, null=True, blank=True)

    payment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.team.team_name} - {self.payment_status}'