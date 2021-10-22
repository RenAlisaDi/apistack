from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAuthorPermission
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated

# Flat models, thin views


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProblemViewSet(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action

        return context


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action

        return context


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

