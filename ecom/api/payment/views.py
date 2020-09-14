from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='xy66nsd58tqz86fz',
    public_key='r6gtk5qsh3jn6c9p',
    private_key='3ef1eae2c92981a827e6e725dbc56b29'
  )
)

def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session.token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False

@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid Session, Please login again'})

    return JsonResponse({'clientToken':gateway.client_token.generate(), 'success':True})

@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Invalid Session, Please login again'})
    
    nonce_from_the_client = request.POST["paymentMethondNonce"]
    amount_from_the_client = request.POST["amount"]

    result = gateway.transaction.sale({
    "amount": amount_from_the_client,
    "payment_method_nonce": nonce_from_the_client,
    #"device_data": device_data_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
    })

    if result.is_success:
        return JsonResponse({
                            'success':result.is_success,
                            'transaction':{'id':result.transaction.id,
                                           'amount':result.transaction.amount
                                          }
                            })

    else:
        return JsonResponse({'error':True, 'success':False})