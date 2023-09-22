from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate,login


# DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer


# BASE APK
from .serializers import MyUser, MyUserSerializerPOST, MyUserSerializerGET


# Create your views here.

class APIUserListView(APIView):

    def get(self, request, format = None):
        users = MyUser.objects.all()
        user_serializer = MyUserSerializerGET(users, many = True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        

class APIUserDelPutView(APIView):

    def get_user(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            return None
        
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        if user is not None:
            user_serializer = MyUserSerializerGET(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        user = self.get_user(pk)
        if user is not None:
            user_serializer = MyUserSerializerPOST(user, data=self.request.data, partial = True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None, user=None):
        user = self.get_user(pk)
        if user is not None:
            # Aquí puedes agregar lógica para verificar permisos si es necesario
            user.delete()
            return Response({"message": "User successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    


class APILoginView(APIView):
    def post(self, request, format=None):
        if 'username' in self.request.data and 'password' in self.request.data:
            username = self.request.data['username']
            password = self.request.data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Autenticación exitosa, inicia sesión
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                token_serializer = AuthTokenSerializer(token)
                return Response({'token': token_serializer.data}, status=status.HTTP_200_OK)
            else:
                # Credenciales incorrectas
                return Response({"message": "Incorrect credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Datos faltantes
            return Response({"message": "Missing credentials"}, status=status.HTTP_400_BAD_REQUEST)


class APIRegisterView(APIView):
    def post(self, request, format=None):
        user_serializer = MyUserSerializerPOST(data=self.request.data)
        if user_serializer.is_valid():
            # Si los datos son válidos, crea un nuevo usuario
            user = user_serializer.save()

            # Genera un token para el nuevo usuario
            token, created = Token.objects.get_or_create(user=user)

            # Serializa el usuario y el token en la respuesta
            user_serializer = MyUserSerializerGET(user)  # Obtén la versión serializada del usuario
            token_serializer = AuthTokenSerializer(token)  # Obtén la versión serializada del token

            return Response({'user': user_serializer.data, 'token': token_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Datos de usuario no válidos
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
