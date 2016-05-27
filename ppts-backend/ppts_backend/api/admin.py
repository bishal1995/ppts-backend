from django.contrib import admin

# Register your models here.
from .models import GuardCredentials,GuardSession

admin.site.register(GuardCredentials)
admin.site.register(GuardSession)