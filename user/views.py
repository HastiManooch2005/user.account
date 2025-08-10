from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
# Create your views here.
class  ListUserAPIView(APIView):
    def get(self,request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users":serializer.data})
    def delete(self, request, id):
        user = MyUser.objects.get(id=id)
        user.delete()
        return Response({'meesage': 'success',})

class RegisterUserAPIView(APIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = serializer.data.get("tokens")
        return Response({'meesage':'success','token':token})

class DeleteUserAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request,id):
        user = MyUser.objects.get(id=id)
        user.delete()
        return Response({'meesage': 'success'})