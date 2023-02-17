from rest_framework.response import Response
from .models import *
from django.conf import settings
import random
import requests
import math
from django.http import HttpResponse
from pypaystack import Transaction, Customer, Plan

transaction = Transaction(authorization_key=settings.PSTACK_SECRET_KEY)

def PaystackPayment(data,profile):
    response  = transaction.verify(data['reference'])
    verified=False
    if response[3]['status'] == 'success':
        verified=True

    # print(response)
    print(verified)
    return verified