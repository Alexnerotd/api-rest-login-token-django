from rest_framework import serializers
from .models import MyUser



class MyUserSerializerGET(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name']


class MyUserSerializerPOST(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ['username','email','password','first_name','last_name']


    
    def create(self, validate_data):
        
        password = self.validated_data.pop('password')

        instance = MyUser(**validate_data)

        if password:
            instance.set_password(password)
        
        instance.save()
        return instance