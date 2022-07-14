from rest_framework import serializers
from .models import Venue

class VenueSerializers(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'