from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from accounts.models import User
# Create your views here.

class SignUpView(CreateAPIView):

    serializer_class = UserSerializer

class AuthDetailView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        user_object = User.objects.get(id=request.user.id)

        serializer_instance = UserSerializer(user_object)

        return Response(serializer_instance.data)
    

