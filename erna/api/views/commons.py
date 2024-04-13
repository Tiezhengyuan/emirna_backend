'''
general information
'''
from rest_framework import viewsets, response, permissions, decorators
from rest_framework.decorators import action
from django.middleware import csrf
from django.http import JsonResponse

from commons.models import CustomUser
from api.serializers import *

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "current":
            return self.request.user
        return super().get_object()

class CommonsViewSet(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['get'])
    def access_info(self, request):
        res = {
            'token': csrf.get_token(request),
        }
        return JsonResponse(res)

def get_token(request):
    res = {
        'csrf_token': csrf.get_token(request),
    }
    return JsonResponse(res)

# todo debugging in the future
# class MethodNameViewSet(viewsets.ModelViewSet):
#     queryset = Method.objects.values_list('method_name', flat=True).distinct()
#     serializer_class = MethodNameSerializer
#     permission_classes = [permissions.IsAuthenticated]