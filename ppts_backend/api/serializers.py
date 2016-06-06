from rest_framework import serializers
from .models import LocationDetails

class LocationDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = LocationDetails
		fields = ( 'location','lattitude','longitude','timestamp' )