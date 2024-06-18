from rest_framework import serializers
from authentication.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email','name', 'tc' ,'password', 'password2')
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    # while serializing we are validating passwords
    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError("Password and Password2 does not match")
        return data
    
    # since we got custom user model so we have to define create 
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']