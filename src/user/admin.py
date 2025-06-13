"""
the admin file of user app
"""
from django.contrib import admin
from .models import Offre, Abonnement

admin.site.register(Offre)
admin.site.register(Abonnement)
