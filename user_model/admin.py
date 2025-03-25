from django.contrib import admin
from .models import User, DynamicData

# Register your models here.
admin.site.register(User)
admin.site.register(DynamicData)