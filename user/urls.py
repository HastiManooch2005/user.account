from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('list/users', ListUserAPIView.as_view(), name='list_users'),
    path('register/user', RegisterUserAPIView.as_view(), name='register_user'),
]