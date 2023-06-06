from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from .serializers import *
from .models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import *
from rest_framework.parsers import FormParser, MultiPartParser


# Create your views here.
@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "farm_id",
                openapi.IN_QUERY,
                description="farm purchased search by farm id",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="farm purchased search by user id",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class FarmPurchasedApi(ListCreateAPIView):
    """
    FarmEvaluation Purchased creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(purchased_by=self.request.user)

    def get_queryset(self):
        farm_id = self.request.query_params.get('farm_id', None)
        user_id = self.request.query_params.get('user_id', None)
        queryset = FarmPurchase.objects.filter(is_delete=False)
        if farm_id:
            queryset = queryset.filter(farm__id=farm_id)
        if user_id:
            queryset = queryset.filter(purchased_by=user_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FarmPurchaseReadSerializer
        else:
            return FarmPurchaseSerializer
