from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404


# DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# BASE APK
from .serializers import MyUser, MyUserSerializerPOST, MyUserSerializerGET


# Create your views here.

class APIUserPostGetView(APIView):

    def get(self, request, format = None):
        users = MyUser.objects.all()
        user_serializer = MyUserSerializerGET(users, many = True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format = None):
        user_serializer = MyUserSerializerPOST(data=self.request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message":"User added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Data invalidate", "errors": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

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

    def put(self, request, pk, format=None, user=None):
        user = self.get_user(pk)
        if user is not None:
            user_serializer = MyUserSerializerPOST(user, data=self.request.data)
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