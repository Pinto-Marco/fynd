from django.contrib import admin
from . import models as customer_models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(customer_models.Fynder)

