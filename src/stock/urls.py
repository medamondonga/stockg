"""
url file of stock app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stockg.generic_crud import (create_customized,
                     list_customized,
                     detail_update_delete_customized)
from .models import (Boutique, PointDeVente, Article,
                     Client, Categorie, Vente, VenteItem,
                     Depense)
from .serializers import (BoutiqueSerializer, PointDeVenteSerializer, ArticleSerializer,
                          CategorieSerializer, CustomerSerializer, ArticleListSerializer,
                          ClientSerializer, VenteItemSerializer, VenteSerializer, VenteListSerializer,
                          DepensesSerializer, DepenseListSerializer)
from .views import (VenteItemByVenteView, produits_les_plus_vendus,
                    statistiques_dashboard, PointDeVenteViewSet,
                    BoutiqueViewSet)

router = DefaultRouter()
router.register(r'pointvente', PointDeVenteViewSet, basename='pointvente')
router.register(r'boutique', BoutiqueViewSet, basename='boutique')

urlpatterns = [
    #endpoints for store
     path("boutiques/",
         list_customized(Boutique, BoutiqueSerializer).as_view(),
         name="list_boutiques"),
     path("boutique/<int:pk>/",
         detail_update_delete_customized(Boutique, BoutiqueSerializer).as_view(),
         name="action-boutique"),

    #endpoints for point de vente
      path('', include(router.urls)),
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
         list_customized(Article, ArticleListSerializer).as_view(),
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
    
     path("client/new/",
          create_customized(Client, ClientSerializer).as_view(),
         name="Creer-client"),
     path("clients/",
          list_customized(Client, ClientSerializer).as_view(),
         name="Liste-Client"),
     path("client/<int:pk>/",
          detail_update_delete_customized(Client, ClientSerializer).as_view(),
          name='action-client'),
     
     path("vente/new/",
          create_customized(Vente, VenteSerializer).as_view(),
          name='creer-vente'),
     path("vente/<int:pk>/",
          detail_update_delete_customized(Vente, VenteSerializer).as_view(),
          name='creer-vente'),
     path("ventes/list/",
          list_customized(Vente, VenteListSerializer).as_view(),
          name='vente-article'),

     path("venteitem/new/",
          create_customized(VenteItem, VenteItemSerializer).as_view(),
          name='creer-vente'),
     path("venteitem/<int:pk>/",
          detail_update_delete_customized(VenteItem, VenteItemSerializer).as_view(),
          name='creer-vente'),
     path("venteitems/",
          VenteItemByVenteView.as_view(), name="venteitems-par-vente"),
     path("venteitem/list/",
          list_customized(VenteItem, VenteItemSerializer).as_view(),
          name='vente-article'),

     path("depense/new/",
          create_customized(Depense, DepensesSerializer).as_view(),
          name='creer_depense'),
     path("depenses/list/",
          list_customized(Depense, DepenseListSerializer).as_view(),
          name='liste-depense'
     ),
     path("depense/<int:pk>/",
          detail_update_delete_customized(Depense, DepensesSerializer).as_view(),
          name="action-depense"),

     path("ventes/top/",
          produits_les_plus_vendus,
          name='top-ventes'),
     path('stats/',
          statistiques_dashboard, 
          name="stat-vente"),

]
