"""
url file of stock app
"""
from django.urls import path
from stockg.generic_crud import (create_customized,
                     list_customized,
                     detail_update_delete_customized)
from .models import (Boutique, PointDeVente, Article,
                     Client, Categorie)
from .serializers import (BoutiqueSerializer, PointDeVenteSerializer, ArticleSerializer,
                          CategorieSerializer, CustomerSerializer)

urlpatterns = [
    #endpoints for store
     path("boutique/new/",
         create_customized(Boutique, BoutiqueSerializer).as_view(),
         name="creation-boutique"),
     path("boutiques/",
         list_customized(Boutique, BoutiqueSerializer).as_view(),
         name="list_boutiques"),
     path("boutique/<int:pk>/",
         detail_update_delete_customized(Boutique, BoutiqueSerializer).as_view(),
         name="action-boutique"),

    #endpoints for point de vente
     path("pointvente/new/",
         create_customized(PointDeVente, PointDeVenteSerializer).as_view(),
         name="creation-point-vente"),
     path("pointventes/",
         list_customized(PointDeVente, PointDeVenteSerializer).as_view(),
         name="liste_point_de_vente"),
     path("pointvente/<int:pk>/",
         detail_update_delete_customized(PointDeVente, PointDeVenteSerializer).as_view(),
         name="action-point-de-vente"),

    #endpoints for articles
     path("article/new/",
         create_customized(Article, ArticleSerializer).as_view(),
         name="New-article"),
     path("articles/",
         list_customized(Article, ArticleSerializer).as_view(),
         name="list-article"),
     path("article/<int:pk>/",
          detail_update_delete_customized(Article, ArticleSerializer).as_view(),
          name="action-article"),

     #endpoints for customers
     path("customer/new/",
          create_customized(Client, CustomerSerializer ).as_view(),
          name="customer-create"),
     path("customer/list/",
          list_customized(Client,CustomerSerializer).as_view(),
          name="customer-list"),
     path("customer/<int:pk>/",
          detail_update_delete_customized(Client, CustomerSerializer).as_view(),
          name="action-customer"),

     #endpoints for categories
     path("categorie/new/",
          create_customized(Categorie, CategorieSerializer).as_view(),
          name="categorie-create"),
     path("categorie/list/",
          list_customized(Categorie, CategorieSerializer).as_view(),
          name="categorie-list"),
     path("categorie/<int:pk>/",
          detail_update_delete_customized(Categorie, CategorieSerializer).as_view(),
          name="action-categorie"),
]
