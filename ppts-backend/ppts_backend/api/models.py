from __future__ import unicode_literals

from django.db import models
import hashlib,time
# Create your models here.

#Guard Credentials
class GuardCredentials(models.Model):
	guard_id = models.AutoField(primary_key=True,unique=True)
	username = models.CharField(max_length=10)
	password = models.CharField(max_length=64)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	designation = models.CharField(max_length=15)
	#Saving the hashed password
	def save(self,*args,**kwargs):
		self.password = hashlib.sha224(self.password).hexdigest()
		super(GuardCredentials,self).save(*args,**kwargs)
	#Returning guard name for visualization
	def __str__(self):
		return self.first_name + ' ' + self.last_name

#Guars Sessions
class GuardSession(models.Model):
	token = models.CharField(max_length=60,primary_key=True,unique=True)
	guard_id = models.ForeignKey(GuardCredentials,on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	login_timestamp = models.DateTimeField(null=True)
	logout_timestamp = models.DateTimeField(null=True)
	#Saving with generated Session ID
	def save(self,*args,**kwargs):
		raw = str(self.login_timestamp) + str(self.guard_id.username)
		self.token = hashlib.sha224(raw).hexdigest()
		super(GuardSession,self).save(*args,**kwargs)
	#Returning Sesion ID for reference
	def __str__(self):
		return self.token

#Location details
class LocationDetails(models.Model):
	location = models.AutoField(primary_key=True)
	token = models.ForeignKey(GuardSession)
	lattitude = models.DecimalField(max_digits=8,decimal_places=6)
	longitude = models.DecimalField(max_digits=8,decimal_places=6)
	timestamp = models.DateTimeField(null=True)
	# Returing token ID for reference
	def __str__(self):
		return self.token.token


#Admin Users
class AdminOfficer(models.Model):
	officer = models.AutoField(primary_key=True,unique=True)
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=64)

# Officer Token
class AdminOfficerToken(models.Model):
	token = models.CharField(max_length=64,primary_key=True)
	officer = models.ForeignKey(AdminOfficer)

	#Token generation
	def save(self,*args,**kwargs):
		raw = str(self.officer.username) + str(time.time())
		self.token = hashlib.sha224(raw).hexdigest()
		super(AdminOfficerToken,self).save(*args,**kwargs)





