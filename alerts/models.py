from django.db import models

class Alert(models.Model):
    # Opções para o status do alerta
    STATUS_CHOICES = [
        ('not_verified', 'Não Verificado'),
        ('verified', 'Verificado'),
    ]

    # Opções para a gravidade do alerta
    SEVERITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
    ]

    # Campos do modelo
    location = models.CharField(max_length=255)  # Local onde o alerta foi registrado
    epidemic = models.CharField(max_length=255)  # Tipo de epidemia (ex.: Dengue, Gripe, etc.)
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='low')  # Gravidade
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_verified')  # Status
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação

    def __str__(self):
        return f"{self.location} - {self.epidemic} ({self.status})"
