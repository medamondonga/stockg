"""
"""
from django.urls import path
from .views import home
from .mixins import create_custom
from .models import User
from .serializers import UserSerializer
urlpatterns = [
    path("home/", home, name="home_accounts"),
    path("signup2/", create_custom(User, UserSerializer).as_view(), name="Creer user2"),

]
