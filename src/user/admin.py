"""
the admin file of user app
"""
from django.contrib import admin
from .models import Offre, Invitation, Abonnement

admin.site.register(Offre)
admin.site.register(Invitation)
admin.site.register(Abonnement)
