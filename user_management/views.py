from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.generics import *

from farm_app.models import Farms
from product.models import Product
from .serializers import *
from .models import (Role, UserRoles, UserBank, UserUpi)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()


class RegisterApi(CreateAPIView):
    """
    New user register api view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    parser_classes = (FormParser, MultiPartParser)
    queryset = User.objects.all()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="name search according to first name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "role",
                openapi.IN_QUERY,
                description="User according to role id",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="User according to status (ACTIVE/IN-ACTIVE) ",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "mobile",
                openapi.IN_QUERY,
                description="User according to mobile",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class UserListApi(ListAPIView):
    """
    List of all user api view
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(is_delete=False)

    def get_queryset(self):
        role = self.request.query_params.get('role')
        status = self.request.query_params.get('status', None)
        mobile = self.request.query_params.get('mobile')
        if status == "IN-ACTIVE":
            status = False
        elif status == "ACTIVE":
            status = True
        else:
            status = None
        if role:
            user_role = UserRoles.objects.filter(role__id=role).values_list('user', flat=True)
            queryset = User.objects.filter(id__in=user_role, is_delete=False)
        else:
            queryset = User.objects.filter(is_delete=False)
        if status is not None:
            queryset = queryset.filter(is_active=status)
        keywords = self.request.query_params.get('search')
        if keywords:
            queryset = queryset.filter(first_name__icontains=keywords)
        if mobile:
            queryset = queryset.filter(mobile__icontains=mobile)
        return queryset


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search user using mobile",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    ),
)
class UserSearchApi(RetrieveAPIView):
    """
    List of all user api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    queryset = User.objects.all()

    def get_object(self):
        mobile = self.request.query_params.get('search')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, mobile=mobile)
        return obj

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, email=self.request.user.email)
    #     return obj


class UserModifyApi(RetrieveUpdateDestroyAPIView):
    """
    Profile Modify api of specific user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileEditSerializer
    parser_classes = (FormParser, MultiPartParser)
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.is_delete = True
        instance.save()


class UserActionApi(RetrieveUpdateDestroyAPIView):
    """
    Profile update, delete and fetch api of current user
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        else:
            return UserProfileEditSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.is_delete = True
        instance.save()


class UserChangePasswordApi(UpdateAPIView):
    """
    change password of user api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer
    queryset = User.objects.filter(is_delete=False)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserStatusApiView(UpdateAPIView):
    """
    change is_active status of user api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserStatusSerializer
    queryset = User.objects.filter(is_delete=False)


class UserPasswordResetApi(UpdateAPIView):
    """
    Reset Password of user api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordResetSerializer
    queryset = User.objects.filter(is_delete=False)


class RoleApi(ListCreateAPIView):
    """
    Role creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer
    pagination_class = PageNumberPagination
    queryset = Role.objects.filter(is_delete=False)


class RoleActionApi(RetrieveUpdateDestroyAPIView):
    """
    Role update, delete and fetch api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleEditSerializer
    queryset = Role.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class UserRoleActionApi(RetrieveDestroyAPIView):
    """
    Profile update, delete and fetch api of current user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRoleSerializer
    queryset = UserRoles.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadUserRoleSerializer
        else:
            return UserRoleSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "role_id",
                openapi.IN_QUERY,
                description="role user according to role id ",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class UserRolesApi(ListCreateAPIView):
    """
    User Role creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRoleSerializer
    pagination_class = PageNumberPagination
    queryset = UserRoles.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadUserRoleSerializer
        else:
            return UserRoleSerializer

    def get_queryset(self):
        queryset = UserRoles.objects.filter(is_delete=False)
        role_id = self.request.query_params.get('role_id')
        if role_id:
            queryset = queryset.filter(role__id=role_id)
        return queryset


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="User according to user id ",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class UserBankApi(ListCreateAPIView):
    """
    create of User Bank Details api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBankSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = UserBank.objects.filter(is_delete=False)
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset


class UserBankEditApi(RetrieveUpdateDestroyAPIView):
    """
     update, delete and fetch api of User Bank Details
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBankSerializer
    queryset = UserBank.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="User according to user id ",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class UserUpiApi(ListCreateAPIView):
    """
    create of User Upi Details api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpiSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = UserUpi.objects.filter(is_delete=False)
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset


class UserUpiEditApi(RetrieveUpdateDestroyAPIView):
    """
     update, delete and fetch api of User Upi Details
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpiSerializer
    queryset = UserUpi.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class AdminStatsApiView(GenericAPIView):
    """
    Admin Stats Api View
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.all()
            active_user = user.filter(is_active=True).count()
            in_active_user = user.filter(is_active=False).count()
            deleted_user = user.filter(is_delete=True).count()
            total_user = user.filter(is_delete=False).count()
            product = Product.objects.all()
            product_count = product.filter(is_delete=False).count()
            deleted_product_count = product.filter(is_delete=True).count()
            farm = Farms.objects.all()
            farm_count = farm.filter(is_delete=False).count()
            deleted_farm_count = farm.filter(is_delete=True).count()
            user_role = UserRoles.objects.all()
            farmer_count = user_role.filter(role__name__iexact="farmer").count()
            buyer_count = user_role.filter(role__name__iexact="buyer").count()
            admin_count = user_role.filter(role__name__iexact="admin").count()

            return Response({
                "active_user": active_user,
                "in_active_user": in_active_user,
                "deleted_user": deleted_user,
                "total_user": total_user,
                "product_count": total_user,
                "deleted_product_count": deleted_product_count,
                "farm_count": farm_count,
                "deleted_farm_count": deleted_farm_count,
                "farmer_count": farmer_count,
                "buyer_count": buyer_count,
                "admin_count": admin_count,

            })
        else:
            return Response({
                "msg": "Authentication failed", "status": 401
            })
