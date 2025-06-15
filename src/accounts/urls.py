"""
urls of account's app
"""
from django.urls import path
from stockg.generic_crud import create_customized, detail_update_delete_customized
from .models import User
from .serializers import UserSerializer, MeSerializer
from .views import get_current_user, AjouterVendeurView, SignupVendeurView, VendeurOwnerView, ListeVendeursDuProprioView
urlpatterns = [
    path("signup/", create_customized(User, UserSerializer).as_view(), name="sign-up"),
    path("me/", get_current_user,
         name='action-utilisateur'),
    path("ajouter-vendeur/", AjouterVendeurView.as_view(), name="ajouter-vendeur"),
    path("signup-vendeur/", SignupVendeurView.as_view(), name="signup-vendeur"),
    path("vendeur/owner/", VendeurOwnerView.as_view(), name="vendeur-owner"),
    path("vendeurs/", ListeVendeursDuProprioView.as_view(), name="vendeurs-proprio"),



]
