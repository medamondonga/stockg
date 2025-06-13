"""
Admin file of stock app
"""
from django.contrib import admin
from .models import Boutique, PointDeVente, Client, Categorie, Article, Vente, Depense

admin.site.register(Boutique)
admin.site.register(Client)
admin.site.register(Categorie)
admin.site.register(Article)
admin.site.register(Vente)
admin.site.register(Depense)
admin.site.register(PointDeVente)

