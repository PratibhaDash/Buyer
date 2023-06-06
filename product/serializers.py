from rest_framework import serializers
from .models import *


class ReadVariantImageSerializer(serializers.ModelSerializer):
    """
    Variant Models serializer
    """

    class Meta:
        model = VariantsImage
        fields = ('id', 'image', 'is_delete')


class VariantSerializer(serializers.ModelSerializer):
    """
    Variant Models serializer
    """
    image = serializers.SerializerMethodField(source='get_image', read_only=True)

    class Meta:
        model = Variant
        fields = (
            'id', 'name', 'product', 'description', 'payment_percentage', 'commission', 'price', 'updated_on',
            'created_on', 'is_delete', 'image')
        read_only_fields = ('id', 'created_on', 'is_delete', 'image')

    def get_image(self, obj):
        return ReadVariantImageSerializer(obj.variant_image.filter(is_delete=False), many=True,
                                          read_only=True, context=self.context).data


class VariantImageSerializer(serializers.ModelSerializer):
    """
    Variant Image Models serializer
    """

    class Meta:
        model = VariantsImage
        fields = ('id', 'variant', 'image', 'is_delete', 'created_on', 'created_by')
        read_only_fields = ('is_delete', 'created_by')


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Models serializer
    """
    variant = VariantSerializer(source='product_variant', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'updated_on', 'created_on',
                  'is_delete', 'image', 'output_per_acer_value', 'output_per_acer_unit', 'expected_output_days',
                  'expected_booking_days',
                  'storage_capacity_days',
                  'created_by', 'variant')
        read_only_fields = ('id', 'is_delete', 'created_by', 'variant')


class CategorySerializer(serializers.ModelSerializer):
    """
    Category Models serializer
    """
    product = ProductSerializer(source='product_category', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'updated_on', 'created_on', 'is_delete', 'product')
        read_only_fields = ('id', 'is_delete', 'product')


class CategoryEditSerializer(serializers.ModelSerializer):
    """
    Category Models serializer
    """

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'updated_on', 'created_on', 'is_delete')
        read_only_fields = ('id', 'is_delete')


class ProductEditSerializer(serializers.ModelSerializer):
    """
    Product Models serializer
    """

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'description', 'image', 'created_by', 'updated_on', 'created_on',
            'is_delete', 'output_per_acer_value', 'output_per_acer_unit', 'expected_output_days',
            'expected_booking_days',
            'storage_capacity_days',)
        read_only_fields = ('id', 'created_on', 'created_by', 'is_delete')
        extra_kwargs = {
            'name': {'required': False},
            'category': {'required': False},
            'description': {'required': False},
            'image': {'required': False},
            'output_per_acer_value': {'required': False},
            'output_per_acer_unit': {'required': False},
            'expected_output_days': {'required': False},
            'expected_booking_days': {'required': False},
            'storage_capacity_days': {'required': False},
        }


class VariantEditSerializer(serializers.ModelSerializer):
    """
    Variant Models serializer
    """

    class Meta:
        model = Variant
        fields = (
            'id', 'name', 'product', 'description', 'payment_percentage', 'commission', 'price', 'updated_on',
            'created_on', 'is_delete')
        read_only_fields = ('id', 'created_on', 'is_delete')
