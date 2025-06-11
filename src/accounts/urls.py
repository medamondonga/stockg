"""
urls of account's app
"""
from django.urls import path
from stockg.generic_crud import create_customized, detail_update_delete_customized
from .views import home
from .models import User
from .serializers import UserSerializer
urlpatterns = [
    path("home/", home, name="home_accounts"),
    path("signup/", create_customized(User, UserSerializer).as_view(), name="sign-up"),
    path("me/<int:pk>/", detail_update_delete_customized(User, UserSerializer).as_view(),
         name='action-utilisateur')

]
