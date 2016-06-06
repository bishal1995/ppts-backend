from django.contrib import admin

# Register your models here.
from .models import GuardCredentials,GuardSession,LocationDetails,AdminOfficer,AdminOfficerToken

admin.site.register(GuardCredentials)
admin.site.register(GuardSession)
admin.site.register(LocationDetails)
admin.site.register(AdminOfficer)
admin.site.register(AdminOfficerToken)
