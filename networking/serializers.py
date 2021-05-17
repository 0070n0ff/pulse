from rest_framework import serializers
from .models import Network

class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Network
        fields = ("name", "cidr")


class NetworkDetailSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    owner = serializers.SlugRelatedField(slug_field="username",read_only=True)
    class Meta:
        model = Network
        exclude =("is_active",)
