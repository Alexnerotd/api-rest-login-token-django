from django.urls import path
from .views import APIUserPostGetView, APIUserDelPutView


urlpatterns = [
    path('users/', APIUserPostGetView.as_view(), name='users-list'),
    path('users/<int:pk>/', APIUserDelPutView.as_view(), name='users-edit'),
]
