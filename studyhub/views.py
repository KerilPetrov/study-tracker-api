from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from studyhub.models import Plan
from studyhub.serializers import PlanCreateSerializer, PlanReadSerializer


class PlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Plan.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PlanReadSerializer
        return PlanCreateSerializer
