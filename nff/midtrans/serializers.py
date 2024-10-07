from rest_framework import serializers
from midtrans.models import Transaction

class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__' 

class MidtransCallbackSerializers(serializers.Serializer):
    transaction_id = serializers.CharField()
    order_id = serializers.CharField()
    status_code = serializers.CharField()
    gross_amount = serializers.CharField()
    transaction_status = serializers.CharField()
    signature_key = serializers.CharField()
    fraud_status = serializers.CharField()