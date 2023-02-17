from rave_python import Rave
from rest_framework.response import Response
from .models import *
from django.conf import settings
import random
import requests
import math
from django.http import HttpResponse

def FlutterWaveRavePayment(data,profile):
    rave = Rave(settings.FLW_PUBLIC_KEY,settings.FLW_SECRET_KEY,usingEnv = False)
    res = rave.Card.verify(data["tx_ref"])

    return res



# def FlutterWaveRavePayment(amount,profile):
#     auth_token= settings.FLW_SECRET_KEY
#     hed = {'Authorization': 'Bearer ' + auth_token}
#     data = {
#             "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
#             "amount":amount,
#             "currency":"KES",
#             # "redirect_url":"http://localhost:8000/callback",
#             "payment_options":"card",
#             "meta":{
#                 "consumer_id":{profile.user.id},
#                 "consumer_mac":"92a3-912ba-1192a"
#             },
#             "customer":{
#                 "email":profile.email,
                
#                 "name":f'{profile.first_name} {profile.second_name}'
#             },
#             "customizations":{
#                 "title":"Soundr",
#                 "description":"SOUNDR package",
#                 # "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
#             }
#             }
#     url = ' https://api.flutterwave.com/v3/payments'
#     response = requests.post(url, json=data, headers=hed)
#     res=response.json()

#     link=res['data']['link']
#     return link