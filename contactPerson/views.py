from twilio.rest import Client
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import ContactPersonSerializer
import os
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication


# Create your views here.


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])

def create_contact(request):
#     data = request.data
#     data['user_id'] = request.user.id
    serializer = ContactPersonSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def send_message(self, request):

#         # Set environment variables for your credentials
#         # Read more at http://twil.io/secure
#         account_sid = "ACf7398f7a58eeaf522145fb5816d7f3ce"
#         auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#         client = Client(account_sid, auth_token)
#         message = client.messages.create(
#         body="Hello from Twilio",
#         from_="+18328645536",
#         to="+250789571856"
#         )
#         print(message.sid)
