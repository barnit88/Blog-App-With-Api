from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes

from accounts.api.serializers import (
    RegistrationSerializer ,
    AccountPropertiesSerializers
)
from rest_framework.authtoken.models import Token
from  rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from accounts.models import Account




@api_view(['POST', ])
@permission_classes((AllowAny,))
def api_registration_view(request):

    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Sucessfully Registered a new User ." 
            data['email'] = account.email 
            data['name'] = account.name 
            data['contact'] = account.contact
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data) 


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializers(account)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def account_update_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializers(account , data = request.data)
        data = {}
        if serializer.is_valid():
            updated = serializer.save()
            data['response'] = "Account update successful"
            data['email'] = updated.email
            data['name'] = updated.name
            data['contact'] = updated.contact
            return Response(data=data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







