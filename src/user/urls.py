from django.urls import path
from .views import SouscrireAbonnementView

urlpatterns = [
    path("souscrire/", SouscrireAbonnementView.as_view(), name="souscrire-abonnement"),
]
