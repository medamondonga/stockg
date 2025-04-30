"""
Here's my user's models
"""
from django.db import models
from django.conf import settings

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
    email_invite = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField()
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES_INVITATIONS, default="sent")

    def __str__(self):
        return f"{self.email_invite}"
    
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
