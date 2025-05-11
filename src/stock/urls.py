"""
url file of stock app
"""
from django.urls import path
from .mixins import (create_customized,
                     list_customized,
                     detail_update_delete_customized)
from .models import Boutique, PointDeVente, Article
from .serializers import BoutiqueSerializer, PointDeVenteSerializer, ArticleSerializer

urlpatterns = [
    #endpoints for store
    path("boutique/new/", create_customized(Boutique, BoutiqueSerializer).as_view(), name="creation-boutique"),
    path("boutiques/", list_customized(Boutique, BoutiqueSerializer).as_view(), name="list_boutiques"),
    path("boutique/<int:pk>/", detail_update_delete_customized(Boutique, BoutiqueSerializer).as_view(), name="action-boutique"),

    #endpoints for point de vente
    path("pointvente/new/", create_customized(PointDeVente, PointDeVenteSerializer).as_view(), name="creation-point-vente"),
    path("pointventes/", list_customized(PointDeVente, PointDeVenteSerializer).as_view(), name="liste_point_de_vente"),
    path("pointvente/<int:pk>/", detail_update_delete_customized(PointDeVente, PointDeVenteSerializer).as_view(), name="action-point-de-vente"),

    #endpoints for articles
    path("articles/", list_customized(Article, ArticleSerializer).as_view(), name="list-article"),
]
