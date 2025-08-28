from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ticket
from .serializers import TicketSerializer, UserMiniSerializer
from django.contrib.auth.models import User

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Ticket.objects.all().order_by("-criado_em")
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=["get"])
    def meus(self, request):
        qs = Ticket.objects.filter(atribuido_a=request.user).order_by("-criado_em")
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=False, methods=["get"])
    def usuarios(self, request):
        """Lista usuários disponíveis para atribuição de tickets"""
        usuarios = User.objects.filter(is_active=True).order_by('username')
        serializer = UserMiniSerializer(usuarios, many=True)
        return Response(serializer.data)
