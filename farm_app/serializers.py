import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from product.serializers import CategorySerializer, VariantSerializer, ProductSerializer
from .models import (Farms, FarmsImage, FarmStage, FarmStagesImage, StagesMaster, FarmerPayment, VariantCommission,
                     FarmLogs)
from product.models import Variant, Product, Category

from user_management.serializers import UserSerializer

User = get_user_model()


class ReadFarmImageSerializer(serializers.ModelSerializer):
    """
    Farm Models serializer
    """

    class Meta:
        model = FarmsImage
        fields = ('id', 'image')


class FarmSerializer(serializers.ModelSerializer):
    """
    Farm Models serializer
    """
    image = serializers.SerializerMethodField(source='get_image', read_only=True, )
    photo = serializers.ImageField(
        help_text='photo which is  add to the farm.', required=False)

    class Meta:
        model = Farms
        fields = (
            'id', 'name', 'address', 'city', 'district', 'state', 'land_value', 'land_unit', 'country', 'pin',
            'is_delete', 'updated_on', 'minimum_sell_value', 'minimum_sell_unit', 'price',
            'expected_harvesting_date', 'created_on', 'category', 'product', 'variant', 'user', 'created_by', 'image',
            'photo')
        read_only_fields = ('is_delete', 'created_by', 'image')
        write_only_fields = ('photo',)

    def get_image(self, obj):
        # You can do more complex filtering stuff here.
        return ReadFarmImageSerializer(obj.farm_image.filter(is_delete=False), many=True, read_only=True,
                                       context=self.context).data

    def _add_photos(self, instance):
        # photo = Role.objects.get(id=self._add_photos)
        FarmsImage.objects.create(farm=instance, created_by=self.context['request'].user, image=self.photo)

    def create(self, validated_data):
        self.photo = validated_data.pop('photo', '')
        instance = super(FarmSerializer, self).create(validated_data)
        if self.photo:
            self._add_photos(instance=instance)
        return instance


class ProductReadSerializer(serializers.ModelSerializer):
    """
    Product Models serializer
    """

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'updated_on', 'created_on',
                  'is_delete', 'image', 'output_per_acer_value', 'output_per_acer_unit', 'expected_output_days',
                  'expected_booking_days', 'storage_capacity_days', 'created_by')
        read_only_fields = ('id', 'is_delete', 'created_by')


class CategoryReadSerializer(serializers.ModelSerializer):
    """
    Category Models serializer
    """

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'updated_on', 'created_on', 'is_delete')
        read_only_fields = ('id', 'is_delete')


class ReadFarmSerializer(serializers.ModelSerializer):
    """
    Farm Models serializer
    """
    image = serializers.SerializerMethodField(source='get_image', read_only=True, )
    category = CategoryReadSerializer()
    variant = VariantSerializer()
    product = ProductReadSerializer()
    user = UserSerializer()
    created_by = UserSerializer()

    class Meta:
        model = Farms
        fields = (
            'id', 'name', 'address', 'city', 'district', 'state', 'land_value', 'land_unit', 'country', 'pin',
            'is_delete', 'updated_on', 'minimum_sell_value', 'minimum_sell_unit', 'price',
            'expected_harvesting_date', 'created_on', 'category', 'product', 'variant', 'user', 'created_by', 'image')
        read_only_fields = ('is_delete', 'created_by', 'image')

    def get_image(self, obj):
        # You can do more complex filtering stuff here.
        return ReadFarmImageSerializer(obj.farm_image.filter(is_delete=False), many=True, read_only=True,
                                       context=self.context).data


class FarmImageSerializer(serializers.ModelSerializer):
    """
    Farm Image Models serializer
    """

    class Meta:
        model = FarmsImage
        fields = ('id', 'farm', 'image', 'is_delete', 'created_on', 'created_by')
        read_only_fields = ('is_delete', 'created_by')


class ReadFarmStageImageSerializer(serializers.ModelSerializer):
    """
    Farm Models serializer
    """

    class Meta:
        model = FarmStagesImage
        fields = ('id', 'image', 'description', 'created_on', 'created_by')


class StageMasterSerializer(serializers.ModelSerializer):
    """
    Stages Models serializer
    """

    class Meta:
        model = StagesMaster
        fields = (
            'id', 'name', 'stage_no', 'product', 'description', 'payment_percentage', 'expected_days', 'is_delete',
            'updated_on', 'created_on', 'created_by',)
        read_only_fields = ('is_delete', 'created_by')


class FarmStageSerializer(serializers.ModelSerializer):
    """
    Farm Stage Models serializer
    """
    image = serializers.SerializerMethodField(source='get_image', read_only=True)
    photo = serializers.ImageField(
        help_text='photo  which is  add to the farm.', required=False)

    class Meta:
        model = FarmStage
        fields = (
            'id', 'stage', 'farm', 'product', 'variant', 'status', 'is_delete', 'updated_on', 'created_on',
            'created_by', 'image', 'photo')
        write_only_fields = ('photo',)
        read_only_fields = ('is_delete', 'created_by', 'image', 'status')

    def get_image(self, obj):
        return ReadFarmStageImageSerializer(obj.farm_stage_image.filter(is_delete=False), many=True,
                                            read_only=True, context=self.context).data

    def _add_photos(self, instance):
        FarmStagesImage.objects.create(farm_stage=instance, description="stage image",
                                       created_by=self.context['request'].user, image=self.photo)

    def create(self, validated_data):
        self.photo = validated_data.pop('photo', '')
        instance = super(FarmStageSerializer, self).create(validated_data)
        if self.photo:
            self._add_photos(instance=instance)
        return instance


class FarmStageStatusSerializer(serializers.ModelSerializer):
    """
    Farm stage status Models serializer to update stages status
    """

    class Meta:
        model = FarmStage
        fields = ('status', 'message')


class UserFarmStageSerializer(serializers.ModelSerializer):
    """
    User Farm Stage Models serializer
    """
    stages = serializers.SerializerMethodField(source='get_stages', read_only=True)
    expected_date = serializers.SerializerMethodField(source='get_expected_date', read_only=True)

    class Meta:
        model = StagesMaster
        fields = (
            'id', 'name', 'stage_no', 'product', 'payment_percentage', 'expected_days', 'is_delete', 'updated_on',
            'created_on', 'created_by', 'expected_date', 'stages')
        read_only_fields = ('is_delete', 'created_by', 'stages')

    def get_stages(self, obj):
        farm_id = self.context['request'].query_params.get('farm_id')
        variant_id = self.context['request'].query_params.get('variant_id')
        return FarmStageSerializer(obj.stage.filter(farm__id=farm_id, variant__id=variant_id), many=True,
                                   read_only=True, context=self.context).data

    def get_expected_date(self, obj):
        farm_id = self.context['request'].query_params.get('farm_id')
        farm = Farms.objects.get(id=farm_id)
        expected_date = farm.expected_harvesting_date
        stages_date = StagesMaster.objects.filter(product=obj.product, stage_no__lte=obj.stage_no,
                                                  is_delete=False).values_list('expected_days', flat=True)
        return expected_date + datetime.timedelta(sum(stages_date))


class FarmStageImageSerializer(serializers.ModelSerializer):
    """
    Farm Stage Image Models serializer
    """

    class Meta:
        model = FarmStagesImage
        fields = ('id', 'farm_stage', 'image', 'description', 'is_delete', 'created_on', 'created_by')
        read_only_fields = ('is_delete', 'created_by')


class FarmerPaymentSerializer(serializers.ModelSerializer):
    """
    Farm Payment Models serializer
    """

    class Meta:
        model = FarmerPayment
        fields = (
            'id', 'stage', 'product', 'variant', 'farm', 'user', 'image', 'amount', 'account', 'payment_on',
            'is_delete', 'updated_on', 'created_on', 'created_by')
        read_only_fields = ('is_delete', 'created_by')


class FarmLogSerializer(serializers.ModelSerializer):
    """
    Farm Log Models serializer
    """
    farm = FarmSerializer()
    created_by = UserSerializer()

    class Meta:
        model = FarmLogs
        fields = "__all__"
