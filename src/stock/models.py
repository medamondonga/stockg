"""
stock models
"""
import random
import string
from django.db import models
from django.conf import settings


CHOICES_ETAT_BOUTIQUE=[
    ("open", "Open"),
    ("closed", "Closed"),
]
CHOICES_SEXE=[
    ("homme", "homme"),
    ("femme", "femme"),
]
CHOICES_TYPE = [
    ("chaussures", "Chaussures"),
    ("vetements", "Vetements"),
    ("sacs", "Sacs"),
    ("autre", "Autre")
]
CHOICES_TRANSFERT = [
    ("pending", "En cours"),
    ("done", "Terminé"),
    ("canceled", "Annulé")
]
CHOICES_COULEUR = [
    ('noir', 'noir'),
    ('blanc', 'blanc'),
    ('gris', 'gris'),
    ('bleu', 'bleu'),
    ('rouge', 'rouge'),
    ('vert', 'vert'),
    ('jaune', 'jaune'),
    ('rose', 'rose'),
    ('orange', 'orange'),
    ('violet', 'violet'),
    ('marron', 'marron'),
    ('beige', 'beige'),
    ('turquoise', 'turquoise'),
    ('bordeaux', 'bordeaux'),
    ('or', 'or')
]
POINTURES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', 
            '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', 
            '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', 
            '46', '47', '48', '49', '50']
TAILLES_VETEMENTS = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL', '5XL', '6XL', '7XL', '8XL']
TAILLES_SACS = ['Petit', 'Moyen', 'Grand','Compact', 'Standard', 'Sport']

class Boutique(models.Model):
    """
    Store class
    """
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom_boutique = models.CharField(max_length=250)
    adresse = models.TextField()
    date_cretation = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=100, choices=CHOICES_ETAT_BOUTIQUE, default="open")

    def __str__(self):
        return f"{self.nom_boutique}"
    
class PointDeVente(models.Model):
    """
    Point de vente classe
    """
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    nom_point_de_vente = models.CharField(max_length=250)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    gerant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name="gerant", unique=True)
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=True, blank=True, related_name="vendeur", unique=True)
    
    def definir_vendeur(self, vendeur):
        if not self.vendeur:
            self.vendeur = vendeur
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"{self.nom_point_de_vente}"
    
class Client(models.Model):
    """
    Class of client
    """
    nom_client = models.CharField(max_length=255)
    prenom_client = models.CharField(max_length=255)
    sexe = models.CharField(max_length=20, choices=CHOICES_SEXE, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom_client} {self.prenom_client}"
    
class Categorie(models.Model):
    """
    categorie models
    """
    nom_categorie = models.CharField(max_length=255)
    type_categorie = models.CharField(max_length=255, choices=CHOICES_TYPE, default="autre")
    
    def get_taille(self):
        """
        to retrieve the sizes
        """
        if self.type_categorie == 'chaussures':
            return POINTURES
        elif self.type_categorie == "vetements":
            return TAILLES_VETEMENTS
        elif self.type_categorie == "sacs":
            return TAILLES_SACS
        else:
            return "Autre"
    
    def __str__(self):
        return f"{self.nom_categorie} {self.type_categorie}"

class Article(models.Model):
    """
    Class of Article
    """
    nom_article = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix_achat_unitaire = models.IntegerField()
    prix_vente_unitaire = models.IntegerField()
    quantite_en_stock = models.IntegerField()
    couleur = models.CharField(max_length=255, choices=CHOICES_COULEUR, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    taille = models.CharField(max_length=50, null=True, blank=True)
    point_de_vente = models.ForeignKey(PointDeVente, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.nom_article}"
    

class Vente(models.Model):
    date_vente = models.DateField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    prix_total_vente = models.IntegerField(null=True, blank=True)
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    point_de_vente = models.ForeignKey(PointDeVente, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f"{self.date_vente} - {self.prix_total_vente} - {self.client}"

class VenteItem(models.Model):
    """
    Vente item class
    """
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='vente_items')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire_recu = models.IntegerField(default=0)
    remise = models.IntegerField(default=0)
    perte = models.IntegerField(default=0)
    benefice = models.IntegerField(default=0)
    total = models.IntegerField()


class Facture(models.Model):
    """
    Model of facture
    """
    date = models.DateField(auto_now_add=True)
    montant_HT = models.DecimalField(max_digits=10, decimal_places=2)
    montant_TTC = models.DecimalField(max_digits=10, decimal_places=2)
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE)

class Transfert(models.Model):
    """
    Model of transfert
    """
    date_transfert = models.DateTimeField(auto_now_add=True)
    point_source = models.ForeignKey(PointDeVente, on_delete=models.CASCADE, related_name='transferts_sortants')
    point_destination = models.ForeignKey(PointDeVente, on_delete=models.CASCADE, related_name='transferts_entrants')
    code = models.CharField(max_length=20, unique=True, blank=True)
    statut_transfert = models.CharField(max_length=50, choices=CHOICES_TRANSFERT, default="pending")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = 'TRF'+''.join(random.choices(string.digits, k=7))
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date_transfert} - {self.point_source} - {self.point_destination} - {self.statut_transfert}"
    
class TransferItem(models.Model):
    """
    Model of tranfert items
    """
    transfert = models.ForeignKey(Transfert, on_delete=models.CASCADE, related_name='items')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField()

class Depense(models.Model):
    """
    Depense models
    """
    point_de_vente = models.ForeignKey(PointDeVente, on_delete=models.CASCADE)
    motif_depense = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
