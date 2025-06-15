from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import User, VendeurAssociation
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password':{'write_only':True}}
    def create(self, validated_data):
            user = User(
                first_name = validated_data["first_name"],
                last_name = validated_data["last_name"],
                username = validated_data["first_name"]+validated_data["last_name"],
                email=validated_data["email"],
                is_owner=True 
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
    
class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_owner', 'is_seller']

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), username=email, password=password)

            if not user:
                raise AuthenticationFailed(_("Cet utilisateur n'existe pas."), code="authorization")
        else:
            raise AuthenticationFailed(_("Email et mot de passe requis."), code="authorization")

        data = super().validate(attrs)
        data["user_id"] = user.id
        data["email"] = user.email
        data["is_seller"] = user.is_seller
        data["is_owner"] = user.is_owner
        return data

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VendeurAssociation  # adapte selon ton app

User = get_user_model()

class AjouterVendeurSerializer(serializers.Serializer):
    vendeur_email = serializers.EmailField(write_only=True)

    def validate_vendeur_email(self, email):
        try:
            vendeur = User.objects.get(email=email, is_seller=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Aucun vendeur avec cet email.")

        if VendeurAssociation.objects.filter(vendeur=vendeur).exists():
            raise serializers.ValidationError("Ce vendeur est déjà lié à un propriétaire.")

        return vendeur  # ⚠️ on retourne l’objet, pas juste l'email

    def create(self, validated_data):
        vendeur = validated_data["vendeur_email"]  # c’est l’objet User
        proprietaire = self.context["request"].user

        return VendeurAssociation.objects.create(vendeur=vendeur, proprietaire=proprietaire)

# serializers.py

class SignupVendeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"]  # ou autre logique
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            is_seller=True
        )
        return user
