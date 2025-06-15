"""
here i create my accounts models
"""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError("Le mot de passe est requis pour un superutilisateur")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


"""class UserAA(AbstractUser):



    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('seller', 'Seller'),
        ('manager', 'Manager'),
    ]
    SEXE = [
        ("homme", "Homme"),
        ("femme", "Femme")
    ]
    USERNAME_FIELD = "email"  # ✅ C’est ça qui dit à Django que le login se fait avec l’email
    REQUIRED_FIELDS = ['first_name', 'last_name']
    username = None
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES,
                            default='owner')
    sexe = models.CharField(max_length=10, choices=SEXE,
                            null=False, blank=False, default='Unknown')


    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.email}"
"""
class User(AbstractUser):
    """
    User's class
    """

    SEXE = [
        ("homme", "Homme"),
        ("femme", "Femme")
    ]
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    sexe = models.CharField(max_length=10, choices=SEXE, null=False, blank=False)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def check_password(self, raw_password):
        """
        Vérifie la correspondance entre le mot de passe brut et celui enregistré.
        """
        return check_password(raw_password, self.password)

    def __str__(self):
        """
        Représentation textuelle de l'utilisateur.
        """
        return f"{self.email}"

class VendeurAssociation(models.Model):
    vendeur = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_seller': True})
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mes_vendeurs", limit_choices_to={'is_owner': True})
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendeur} (lié à {self.proprietaire})"
