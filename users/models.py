from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('HealthAuthority', 'Autoridade de Saúde'),
        ('SocietyUser', 'Usuário da Sociedade'),
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=100, blank=True, null=True)  # Apenas para Autoridade de Saúde
    preferences = models.JSONField(default=dict, blank=True, null=True)  # Apenas para Usuário da Sociedade

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Alterar related_name para evitar conflito
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Alterar related_name para evitar conflito
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Métodos para verificar o tipo de usuário
    def is_health_authority(self):
        return self.role == 'HealthAuthority'

    def is_society_user(self):
        return self.role == 'SocietyUser'
