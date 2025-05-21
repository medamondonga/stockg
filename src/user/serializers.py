from rest_framework import serializers

from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['email_invite', 'point_de_vente']



               

