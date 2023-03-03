from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.serializers import UserRegistationSerializer,UserLoginSerializer,UserProfileSerializer,SendPasswordToEmail,UserResertPasswordSerializer
from django.contrib.auth import authenticate
from api.renderers import UserRender
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# generate token mannuly
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
# Create your views here.
class UserRegistationView(APIView):
    def post(self,request,format=None):
        serializer=UserRegistationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registation succesfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login succesfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({'error':{'non_field_error':['Email or password is not valid' ]}},status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)        

class UserProfileView(APIView):
    renderer_classes=[UserRender]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        if serializer.is_valid(raise_exception="True"):
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        
class UserResetPassword(APIView):
    renderer_classes=[UserRender]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserResertPasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change succesfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class SendpasswordEmail(APIView):
    renderer_classes=[UserRender]
    def post(self,request,format=None):
        serializer=SendPasswordToEmail(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Resend link send, Plese check your email'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_200_OK)
    
class PasswordResertView(APIView):
    renderer_classes=[UserRender]
    def post(self,request,udi,token,format=None):
        serializer=UserResertPasswordSerializer(data=request.data,context={'udi':udi,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Succfully!!!'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_200_OK)
            
            


