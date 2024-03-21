from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from rna_seq.models import ProjectExecution
from api.serializers import ProjectExecutionSerializer


class ProjectExecutionViewSet(viewsets.ModelViewSet):
  serializer_class = ProjectExecutionSerializer
  queryset = ProjectExecution.objects.all()
  permission_classes = [permissions.IsAuthenticated,]

