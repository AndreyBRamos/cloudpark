from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket

class UserMiniSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]

class TicketSerializer(serializers.ModelSerializer):
    criado_por_info = UserMiniSerializer(source="criado_por", read_only=True)
    atribuido_a_info = UserMiniSerializer(source="atribuido_a", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id", "titulo", "descricao", "prioridade", "setor", "status",
            "criado_por", "atribuido_a", "criado_em", "atualizado_em",
            "criado_por_info", "atribuido_a_info"
        ]
        read_only_fields = ["criado_por"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["criado_por"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        new_status = validated_data.get("status", instance.status)
        if instance.status != "RESOLVIDO" and new_status == "RESOLVIDO":
            if not request or not request.user.is_authenticated:
                raise serializers.ValidationError("Autenticação necessária.")
            role = getattr(getattr(request.user, "profile", None), "role", None)
            if role != "TECNICO":
                raise serializers.ValidationError("Apenas um técnico pode marcar como 'Resolvido'.")
        return super().update(instance, validated_data)
