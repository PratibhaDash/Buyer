from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import (IsAuthenticated, AllowAny)
from .serializers import *
from .models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import *
from rest_framework.parsers import FormParser, MultiPartParser


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="farm search using user id",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class FarmApi(ListCreateAPIView):
    """
    Farm creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmSerializer
    pagination_class = PageNumberPagination
    parser_classes = (FormParser, MultiPartParser)
    queryset = Farms.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        # The request user is set as created_by automatically.
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = Farms.objects.filter(user=user_id, is_delete=False)
        else:
            queryset = Farms.objects.filter(is_delete=False)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadFarmSerializer
        else:
            return FarmSerializer


class FarmEditApi(RetrieveUpdateDestroyAPIView):
    """
    Farm retrieve, update, destroy api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmSerializer
    pagination_class = PageNumberPagination
    queryset = Farms.objects.filter(is_delete=False)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadFarmSerializer
        else:
            return FarmSerializer


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="farm search using name",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class UserFarmApi(ListAPIView):
    """
    Farm List api view of current user
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search = self.request.query_params.get('search')
        query = Farms.objects.filter(is_delete=False, user=self.request.user)
        if search:
            query = query.filter(name__icontains=search)
        return query


class FarmImageApi(ListCreateAPIView):
    """
    Farm creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmImageSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = PageNumberPagination
    queryset = FarmsImage.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        # The request user is set as created_by automatically.
        serializer.save(created_by=self.request.user)


class FarmImageEditApi(RetrieveDestroyAPIView):
    """
    Farm image retrieve destroy api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmImageSerializer
    queryset = FarmsImage.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "farm_id",
                openapi.IN_QUERY,
                description="farm stage search",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="farm stage search",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "variant_id",
                openapi.IN_QUERY,
                description="farm stage search",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class FarmStageApiView(ListCreateAPIView):
    """
    Farm stage creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmStageSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        farm_id = self.request.query_params.get('farm_id')
        variant_id = self.request.query_params.get('variant_id')
        product_id = self.request.query_params.get('product_id')
        if farm_id and variant_id and product_id:
            queryset = FarmStage.objects.filter(farm__id=farm_id, variant__id=variant_id, product__id=product_id,
                                                is_delete=False)
        elif farm_id:
            queryset = FarmStage.objects.filter(is_delete=False, farm__id=farm_id)
        else:
            queryset = FarmStage.objects.filter(is_delete=False)
        return queryset


class FarmStageStatusApiView(UpdateAPIView):
    """
    Farm stage status update api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmStageStatusSerializer
    pagination_class = PageNumberPagination
    queryset = FarmStage.objects.all()


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="stage search by product ID",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class StageMasterApiView(ListCreateAPIView):
    """
    Farm stage creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = StageMasterSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = StagesMaster.objects.filter(product__id=product_id, is_delete=False)
        else:
            queryset = StagesMaster.objects.filter(is_delete=False)
        return queryset


class FarmStageImageApiView(ListCreateAPIView):
    """
    Farm Stage image creation and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmStageImageSerializer
    parser_classes = (FormParser, MultiPartParser)
    pagination_class = PageNumberPagination
    queryset = FarmStagesImage.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class FarmStageImageEditApi(RetrieveDestroyAPIView):
    """
    Farm Stage image retrieve destroy api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmStageImageSerializer
    queryset = FarmStagesImage.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "farm_id",
                openapi.IN_QUERY,
                description="UserFarmStage search",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="farm stages search by product_id",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                "variant_id",
                openapi.IN_QUERY,
                description="farm stages search by variant_id",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    ),
)
class UserFarmStageApi(ListAPIView):
    """
    FarmStage of user List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFarmStageSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        queryset = StagesMaster.objects.filter(product__id=product_id, is_delete=False)
        return queryset


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "stage",
                openapi.IN_QUERY,
                description="farmer payment according to stage ",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "product",
                openapi.IN_QUERY,
                description="farmer payment according to product",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "farm",
                openapi.IN_QUERY,
                description="farmer payment according to  farm ",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="farmer payment according to user ",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class FarmerPaymentApi(ListCreateAPIView):
    """
    Farmer payment create and List api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmerPaymentSerializer
    pagination_class = PageNumberPagination
    parser_classes = (FormParser, MultiPartParser)
    queryset = FarmerPayment.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        # The request user is set as created_by automatically.
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        stage_id = self.request.query_params.get('stage')
        product_id = self.request.query_params.get('product')
        farm_id = self.request.query_params.get('farm')
        queryset = FarmerPayment.objects.filter(is_delete=False)
        if user_id:
            queryset = queryset.filter(user=user_id)
        if stage_id:
            queryset = queryset.filter(stage=stage_id)
        if product_id:
            queryset = queryset.filter(product=product_id)
        if farm_id:
            queryset = queryset.filter(farm=farm_id)

        return queryset


class FarmerPaymentEditApi(RetrieveUpdateDestroyAPIView):
    """
    Farmer payment retrieve, update, destroy api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmerPaymentSerializer
    parser_classes = (FormParser, MultiPartParser)
    queryset = FarmerPayment.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


@method_decorator(
    name="get",  # change is here
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "farm_id",
                openapi.IN_QUERY,
                description=" Farm Logs search by farm ID",
                type=openapi.TYPE_STRING,
            )
        ]
    ),
)
class FarmLogsApi(ListAPIView):
    """
    Farm logs list api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmLogSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        farm_id = self.request.query_params.get('farm_id')
        queryset = FarmLogs.objects.filter(is_delete=False)
        if farm_id:
            queryset = queryset.filter(farm=farm_id)
        return queryset


class FarmLogDetailsApi(RetrieveDestroyAPIView):
    """
    Farm logs retrieve, destroy api view
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmLogSerializer
    queryset = FarmLogs.objects.all()

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
