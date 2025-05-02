from django.urls import path
from .views import home
from .mixins import SignUpView

urlpatterns = [
    path("home/", home, name="home_accounts"),
    path("create/", SignUpView.as_view(), name="sign_up",)
]
