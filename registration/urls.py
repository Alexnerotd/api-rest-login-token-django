from django.urls import path
from .views import APIUserListView, APIUserDelPutView, APILoginView, APIRegisterView


urlpatterns = [
    path('users/', APIUserListView.as_view(), name='users-list'),
    path('users/<int:pk>/', APIUserDelPutView.as_view(), name='users-edit'),
    path('users/register/', APIRegisterView.as_view(), name='register'),
    path('users/login/', APILoginView.as_view(), name='login'),
]
