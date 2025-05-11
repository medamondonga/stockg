"""
urls of account's app
"""
from django.urls import path
from stockg.generic_crud import create_customized
from .views import home
from .models import User
from .serializers import UserSerializer
urlpatterns = [
    path("home/", home, name="home_accounts"),
    path("signup2/", create_customized(User, UserSerializer).as_view(), name="Creer user2"),

]
