"""
url file of stock app
"""
from django.urls import path
from .mixins import (CreateBoutique,ListBoutique, BoutiqueAction,
                     CreatePointDeVente, ListPointVente, PointVenteAction,
                     ArticleList, )

urlpatterns = [
    #endpoints for store
    path("boutique/new/", CreateBoutique.as_view(), name="creation-boutique"),
    path("boutiques/", ListBoutique.as_view(), name="list_boutiques"),
    path("boutique/<int:pk>/", BoutiqueAction.as_view(), name="action-boutique"),

    #endpoints for point de vente
    path("pointvente/new", CreatePointDeVente.as_view(), name="creation-point-vente"),
    path("pointventes/", ListPointVente.as_view(), name="liste_poiny_de_vente"),
    path("pointvente/<int:pk>/", PointVenteAction.as_view(), name="action-point-de-vente"),

    #endpoints for articles
    path("articles/", ArticleList.as_view(), name="list-article"),
]
