from rest_framework import serializers
from location.models import State, LocalGovernmentArea


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalGovernmentArea
        fields = '__all__'
