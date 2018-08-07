from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User


# Create your views here.

class UserCreate(viewsets.ViewSet):
    '''
    creates the user
    '''

    def post(self,request, format='json'):
        serializer = UserSerializer(data=request.data,)

        if serializer.is_valid():
            user = serializer.save()

            if user:
                return Response(serializer.data,
                                status = status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status = status.HTTP_400_BAD_REQUEST)

    def get(self,request,format = None):
        username = request.query_params.get('username',None)
        pk = request.query_params.get('pk',None)

        user  = None

        if username:
            user = User.objects.get(username=username)
            pass

        if pk:
            user = User.objects.get(pk = pk)
            pass

        if not user:
            return Response({'error':'missing field'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)

        return Response(serializer.data)