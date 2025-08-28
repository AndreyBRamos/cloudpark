from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (("ATENDENTE", "Atendente"), ("TECNICO", "Técnico"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="ATENDENTE")

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Ticket(models.Model):
    PRIORIDADE_CHOICES = (("BAIXA", "Baixa"), ("MEDIA", "Média"), ("ALTA", "Alta"))
    STATUS_CHOICES = (
        ("ABERTO", "Aberto"),
        ("EM_ATENDIMENTO", "Em Atendimento"),
        ("RESOLVIDO", "Resolvido"),
        ("CANCELADO", "Cancelado"),
    )

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default="MEDIA")
    setor = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ABERTO")
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets_criados")
    atribuido_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_atribuidos")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.status}] {self.titulo}"
