"""
Here's my user's models
"""
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from stock.models import PointDeVente

STATUT_CHOICES_INVITATIONS = [
    ("refused", "refused"),
    ("accepted", "accepted"),
    ("sent", "sent"),
    ("expired", "expired")
]
STATUT_CHOICES_ABONNEMENTS = [
    ("active", "active"),
    ("terminated", "terminated"),
    ("not_active", "not_active"),
]



class Invitation(models.Model):
    """
    the invitation class
    """
    token = models.UUIDField(default=uuid4, unique=True, editable=False)
    email_invite = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES_INVITATIONS, default="sent")
    point_de_vente = models.ForeignKey(PointDeVente,on_delete=models.CASCADE)

    def is_valid(self, token):
        return self.statut == "sent" and self.date_expiration > timezone.now() and self.token == token
    
    def accepted(self):
        if self.statut == "sent":
            self.statut = "accepted"
            self.save()
            return True
        return False
    


    def save(self, *args,**kwargs):
        if not self.date_expiration :
            self.date_expiration = timezone.now() + timedelta(hours=1)
        super().save(*args,**kwargs)
    
    
    
 
    def __str__(self):
        return f"{self.email_invite} {self.statut}"
    
class Offre(models.Model):
    """
    the offre class
    """
    nom_offre = models.CharField(max_length=250)
    description = models.TextField()
    prix_mensuel = models.DecimalField(max_digits=5,decimal_places=2)
    nombre_boutique_max = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.nom_offre}"

class Abonnement(models.Model):
    """
    the abonnement class
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES_ABONNEMENTS, default="not_active")

    def __str__(self):
        return f"{self.user} - {self.offre}"
