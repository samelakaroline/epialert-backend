from django.contrib import admin
from .models import User

# Registro do modelo User no admin
admin.site.register(User)
