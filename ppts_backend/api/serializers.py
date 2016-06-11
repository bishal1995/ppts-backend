from rest_framework import serializers
from .models import LocationDetails,GuardCredentials,GuardSession

class LocationDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = LocationDetails
		fields = ( 'location','lattitude','longitude','arivaldate','arivaltime' )

class GuardCredentialsSerializer(serializers.ModelSerializer):
	class Meta:
		model = GuardCredentials
		fields = ( 'guard_id' , 'first_name' , 'last_name' )

class GuardSessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = GuardSession
		fields = ( 'token','guard_id','active','logindate','logintime','logoutdate','logouttime')
		
