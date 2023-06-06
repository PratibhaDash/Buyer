from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FarmPurchase
from farm_app.serializers import FarmSerializer, ProductReadSerializer, CategoryReadSerializer
from product.serializers import VariantSerializer
from user_management.serializers import UserSerializer

User = get_user_model()


class FarmPurchaseSerializer(serializers.ModelSerializer):
    """
    FarmPurchase Models serializer
    """

    class Meta:
        model = FarmPurchase
        fields = (
            'id', 'farm', 'category', 'product', 'variant', 'purchased_value', 'purchased_unit',
            'price', 'is_delete', 'updated_on', 'created_on', 'purchased_by'
        )
        read_only_fields = ('is_delete', 'purchased_by', 'price')

    def create(self, validated_data):
        purchased_unit = validated_data['purchased_unit'].lower()  # converting grams and quantiles to kg
        purchased_value = validated_data['purchased_value']
        if purchased_unit == 'grams':
            purchased_value = purchased_unit / 1000
        elif purchased_unit == 'quantiles':
            purchased_value = purchased_unit * 1000
        price = purchased_value * validated_data['farm'].price
        commission = validated_data['variant'].commission
        value = (price * commission) / 100
        validated_data['price'] = price + value
        return super(FarmPurchaseSerializer, self).create(validated_data)


class FarmPurchaseReadSerializer(serializers.ModelSerializer):
    """
    FarmPurchase Models serializer
    """
    farm = FarmSerializer()
    category = CategoryReadSerializer()
    product = ProductReadSerializer()
    variant = VariantSerializer()
    purchased_by = UserSerializer()

    class Meta:
        model = FarmPurchase
        fields = (
            'id', 'farm', 'category', 'product', 'variant', 'purchased_value', 'purchased_unit',
            'price', 'is_delete', 'updated_on', 'created_on', 'purchased_by'
        )
        read_only_fields = ('is_delete', 'purchased_by')
