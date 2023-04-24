from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from serModel.serializers import UploadedFileSerializer
from .apps import SermodelConfig
import numpy as np
import librosa
from sklearn.preprocessing import OneHotEncoder
import os
from twilio.rest import Client
from contactPerson.models import ContactPerson
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication
from rest_framework import status
from playsound import playsound


def get_feature(file_path: str, mfcc_len: int = 39, mean_signal_length: int = 100000):

    signal, fs = librosa.load(file_path)
    s_len = len(signal)

    if s_len < mean_signal_length:
        pad_len = mean_signal_length - s_len
        pad_rem = pad_len % 2
        pad_len //= 2
        signal = np.pad(signal, (pad_len, pad_len + pad_rem),
                        'constant', constant_values=0)
    else:
        pad_len = s_len - mean_signal_length
        pad_len //= 2
        signal = signal[pad_len:pad_len + mean_signal_length]
    mfcc = librosa.feature.mfcc(y=signal, sr=fs, n_mfcc=39)
    mfcc = mfcc.T
    feature = mfcc
    return feature


# def send_message(sender_name, receiver_name, sender_no, receiver_no):
#     account_sid = "ACf7398f7a58eeaf522145fb5816d7f3ce"
#     auth_token = os.getenv("TWILIO_AUTH_TOKEN")
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body='Hello, ' + str(receiver_name) + '. We have sensed that your friend ' +
#         str(sender_name) +
#         ' of phone number ' + str(sender_no) + ' might be in danger. Kindly take action.',
#         from_=sender_no,
#         to=receiver_no
#     )
#     print(message.sid)

def send_message(sender_name, sender_no, receivers):
    account_sid = "ACf7398f7a58eeaf522145fb5816d7f3ce"
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    for receiver in receivers:
        receiver_name = receiver.name
        receiver_no = receiver.phone
        print('Name: ' + str(receiver_name) + ', Phone: ' + str(receiver_no))
        message = client.messages.create(
            body='Hello, ' + str(receiver_name) + '. We have sensed that your friend ' +
            str(sender_name) +
            ' of phone number ' + str(sender_no) + ' might be in danger. Kindly take action.',
            from_=sender_no,
            to=receiver_no
        )
        print(message.sid)


# Create your views here.

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def predict(request):

    sender_name = request.user.username
    sender_no = request.user.phone_number
    # receiver = ContactPerson.objects.get(user=request.user.id)
    receivers = ContactPerson.objects.filter(user=request.user.id)
    # receiver_name = receiver.name
    # receiver_no = receiver.phone

    serializer = UploadedFileSerializer(data=request.data)

    model = SermodelConfig.ser_model

    emotions = [['angry', 'calm', 'disgust', 'fear', 'happy',
                 'neutral', 'sad', 'surprise']]  # Emotions as ordered by the training one hot encoder

    # One hot encode the emotions
    encoder = OneHotEncoder()
    encoder.fit_transform(np.array(emotions).reshape(-1, 1)).toarray()

    # Driver Code

    if serializer.is_valid():
        uploaded_file = serializer.save()
        # saved_audio = request.data['file']
        saved_audio2 = uploaded_file.file.path
        # process the file with the machine learning model
        if saved_audio2 is not None:

            print("Saved audio: " + str(saved_audio2))
            playsound(saved_audio2)
            print('playing sound using  playsound')

            X = get_feature(saved_audio2)
            X = np.expand_dims(X, axis=1)  # New shape will be (None, 1, 39)
            X = np.tile(X, (1, 196, 1))  # New shape will be (None, 196, 39)

            y = model.model.predict(X)

            emotion = encoder.inverse_transform(y)[0][0]

            if emotion == 'fear' or emotion == 'angry':
                send_message(sender_name,
                             sender_no, receivers)

            # delete the file when done
            os.remove(uploaded_file.file.path)

            return Response({"message": "Success", "data": emotion})

        # return Response({'result': result}, status=status.HTTP_200_OK)
    else:

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # saved_audio = os.path.join(BASE_DIR,'serModel/model/03-01-03-01-02-01-01.wav')

    # saved_audio = os.path.join(BASE_DIR,'serModel/model/03-01-03-01-02-01-01.wav')
