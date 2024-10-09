from rest_framework.response import Response
from rest_framework.views import APIView
from .data import generate_price, generate_category_name
from .models import Transaction
from .serializers import MidtransCallbackSerializers, TransactionSerializers
from team.models import Team
from django.db.transaction import atomic
from uuid import UUID
from dotenv import load_dotenv
import uuid
import midtransclient
import os
import hashlib

load_dotenv()

class CreatePaymentAPI(APIView):
    def post(self, request):
        team_id = request.data['team_id']

        if not Team.objects.filter(id=team_id).exists():
            return Response({
                'message': 'Team not found'
            }, status=400)

        team_obj = Team.objects.get(id=team_id)

        team_owner_obj = team_obj.owner

        transaction_id = str(uuid.uuid4())
        gross_amount = generate_price(team_obj.sub_category)

        with atomic():
            snap = midtransclient.Snap(
                # Set to true if you want Production Environment (accept real transaction).
                is_production=os.getenv('MIDTRANS_IS_PRODUCTION', 'False') == 'True',
                server_key=os.getenv('MIDTRANS_SERVER_KEY')
            )

            snap_transaction = snap.create_transaction({
                "transaction_details": {
                    "order_id": transaction_id,
                    "gross_amount": gross_amount
                },
                "credit_card": {
                    "secure": True
                },
                "customer_details": {
                    "first_name": f'{team_obj.team_name} -',
                    "last_name": team_obj.institution,
                    "email": team_owner_obj.email,
                    "phone": team_obj.phone_number
                },
                "item_details": [
                    {
                        "id": team_obj.sub_category,
                        "price": gross_amount,
                        "quantity": 1,
                        "name": generate_category_name(team_obj.sub_category)
                    }
                ],
                "expiry": {
                    "unit": "hours",
                    "duration": 24
                },
            })
            snap_transaction_token = snap_transaction['token']
            snap_redirect_url = snap_transaction['redirect_url']

            transaction = Transaction.objects.create(
                team=team_obj,
                transaction_id=transaction_id,
                midtrans_token=snap_transaction_token,
                gross_amount=gross_amount,
                redirect_url=snap_redirect_url
            )
            transaction.save()

        return Response({
            'message': 'Payment created',
            'data': {
                'order_id': transaction_id,
                'gross_amount': gross_amount,
                'redirect_url': snap_redirect_url
            }
        })
    

class PaymentCallbackAPI(APIView):
    def post(self, request):
        callback_data = MidtransCallbackSerializers(data=request.data)
        callback_data.is_valid(raise_exception=True)

        callback_data = callback_data.data

        transaction_validity =  self.verify_transaction(
            order_id=callback_data['order_id'],
            status_code=callback_data['status_code'],
            gross_amount=callback_data['gross_amount'],
            callback_signature_key=callback_data['signature_key']
        )
        
        if not transaction_validity:
            return Response({'message': 'Invalid signature key'})
        order_id = callback_data['order_id']

        # If the order_id is a test or doesn't match valid criteria, return early
        
        if order_id.startswith("payment_notif_test"):
            return Response({
                'message': 'Test order, no further processing'
            })
        
        with atomic():  # Ensure database atomicity
            # Check if the order exists
            transaction = Transaction.objects.filter(transaction_id=order_id).first()

            if not transaction:
                return Response({
                    'message': 'Transaction not found'
                }, status=404)
        
    
            if callback_data['transaction_status'] == 'capture':
                if callback_data['fraud_status'] == 'accept':
                    # Update payment status to success
                    transaction.payment_status = 'Success'
                    transaction.save()
                    transaction.team.is_paid = True
                    transaction.team.save()
            elif callback_data['transaction_status'] == 'settlement':
                # Settle the transaction
                transaction.payment_status = 'Success'
                transaction.save()
                transaction.team.is_paid = True
                transaction.team.save()
            elif callback_data['transaction_status'] in ['cancel', 'deny', 'expire']:
                # Handle failed transaction statuses
                transaction.payment_status = 'Expired'
                transaction.team.delete()
                #transaction.save()
            elif callback_data['transaction_status'] == 'pending':
                # Handle pending payments, you might not want to update anything here
                pass
        
        transaction_serializer = TransactionSerializers(transaction)
        return Response({
            'message': 'Payment callback handled successfully',
            'data': transaction_serializer.data
        }, status=200)

    
    def verify_transaction(self, order_id, status_code, gross_amount, callback_signature_key):
        server_key = os.getenv('MIDTRANS_SERVER_KEY')

        data = f'{order_id}{status_code}{gross_amount}{server_key}'

        sha512 = hashlib.sha512()
        sha512.update(data.encode('utf-8'))
        return sha512.hexdigest() == callback_signature_key
