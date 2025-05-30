from rest_framework import serializers
from .models import User




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
                email=validated_data["email"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user