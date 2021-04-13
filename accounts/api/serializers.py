from rest_framework import serializers

from accounts.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'} , write_only=True)
    
    class Meta:
        model = Account
        fields = ['name'  ,'contact' ,'email' ,'password' , 'password2']
        extra_kwargs = {
            'password1' : {'write_only' : True } #Aru leh nadekhos bhanera
        }
    
    def save(self):
        account = Account(
            email = self.validated_data['email'],
            name = self.validated_data['name'],
            contact = self.validated_data['contact'], 
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password' : "password didnt matched."})

        account.set_password(password)
        account.save()
        return account


#serializer for acount update
class AccountPropertiesSerializers(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['pk' , 'email' , 'name' ,'contact']
