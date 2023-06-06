from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .models import Category, Product, Variant


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search Category using name",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class CategoryApi(generics.ListCreateAPIView):
    """
    create of Category api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    queryset = Category.objects.filter(is_delete=False)

    def get_queryset(self):
        queryset = Category.objects.filter(is_delete=False)
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        return queryset


class CategoryDeletedApi(generics.ListAPIView):
    """
    Delete of Category api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    queryset = Category.objects.filter(is_delete=True)

    def get_queryset(self):
        queryset = Category.objects.filter(is_delete=True)
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        return queryset


class CategoryEditApi(generics.RetrieveUpdateDestroyAPIView):
    """
     update, delete and fetch api of Category
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_delete=False)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search Product using name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "category_id",
                openapi.IN_QUERY,
                description="Search Product using Category id",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class ProductApi(generics.ListCreateAPIView):
    """
    create of Product api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Product.objects.filter(is_delete=False)
        keywords = self.request.query_params.get('search')
        category_id = self.request.query_params.get('category_id')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset


class ProductDeletedApi(generics.ListAPIView):
    """
    Delete of Product api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    parser_classes = (FormParser, MultiPartParser)

    def get_queryset(self):
        queryset = Product.objects.filter(is_delete=True)
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        return queryset


class ProductEditApi(generics.RetrieveUpdateDestroyAPIView):
    """
     update, delete and fetch api of Product
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    parser_classes = (FormParser, MultiPartParser)
    queryset = Product.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search Variant using name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="Search Product using product id",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class VariantApi(generics.ListCreateAPIView):
    """
    create of Variant api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VariantSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Variant.objects.filter(is_delete=False)
        product_id = self.request.query_params.get('product_id')
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        return queryset


class VariantDeletedApi(generics.ListAPIView):
    """
    Delete of Variant api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VariantSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Variant.objects.filter(is_delete=True)
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(name__icontains=keywords)
        return queryset


class VariantEditApi(generics.RetrieveUpdateDestroyAPIView):
    """
     update, delete and fetch api of Variant
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VariantEditSerializer
    queryset = Variant.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class VariantImageApi(ListCreateAPIView):
    """
    Variant Image creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VariantImageSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = PageNumberPagination
    queryset = VariantsImage.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class VariantImageDeletedApi(ListAPIView):
    """
    Variant Image Delete List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VariantImageSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = PageNumberPagination
    queryset = VariantsImage.objects.filter(is_delete=True)


class VariantImageEditApi(RetrieveDestroyAPIView):
    """
    Variant image retrieve destroy api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = VariantImageSerializer
    queryset = VariantsImage.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
