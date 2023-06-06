from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .models import (Role, UserRoles, UserBank, UserUpi, )
import re
from datetime import date, timedelta

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    """
    Role Models serializer
    """

    class Meta:
        model = Role
        fields = ('id', 'name', 'status', 'created_on')
        read_only_fields = ('id', 'created_on', 'status')


class RoleEditSerializer(serializers.ModelSerializer):
    """
    Role Models serializer
    """

    class Meta:
        model = Role
        fields = ('id', 'name', 'status', 'created_on', 'is_delete')
        read_only_fields = ('id', 'created_on', 'is_delete')


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Role Models serializer
    """

    class Meta:
        model = UserRoles
        fields = ('id', 'user', 'role', 'status', 'created_on')


class UserViewRoleSerializer(serializers.ModelSerializer):
    """
    Role Models serializer
    """
    role = RoleSerializer()

    class Meta:
        model = UserRoles
        fields = ('id', 'role', 'status', 'created_on')


class UserSerializer(serializers.ModelSerializer):
    """
    Register new user model serializer
    """
    user_role = UserViewRoleSerializer(many=True, read_only=True)
    role_pk = serializers.IntegerField(
        help_text=_('role primary keys to which to add the user.'), required=False)
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'mobile', 'email', 'password', 'dob', 'id1', 'id2', 'image', 'address',
            'is_active', 'last_login', 'date_joined', 'user_role', 'role_pk', 'is_delete', 'age')
        write_only_fields = ('password', 'role_pk')
        read_only_fields = ('is_active', 'last_login', 'date_joined', 'user_role', 'is_delete', 'age')

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.
        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def validate_mobile(self, value: int) -> int:
        """
        :param value: mobile of a user
        verify user mobile number is valid or not.
        """
        valid = re.match("[6-9][0-9]{9}", str(value))
        if not valid:
            raise serializers.ValidationError("Mobile number is not in valid format")
        return value

    def _add_roles(self, instance):
        role = Role.objects.get(id=self.role_pk)
        UserRoles.objects.create(user=instance, role=role)

    def create(self, validated_data):
        self.role_pk = validated_data.pop('role_pk', '')
        instance = super(UserSerializer, self).create(validated_data)
        if self.role_pk:
            self._add_roles(instance=instance)
        return instance

    def get_age(self, obj):
        return (date.today() - obj.dob) // timedelta(days=365.2425)


class UserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        required=True, style={'input_type': 'old password'}, write_only=True
    )
    new_password = serializers.CharField(
        required=True, style={'input_type': 'new password'}, write_only=True
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-detail'}
        }
        fields = (
            'old_password', 'new_password')
        model = User

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-status'}
        }
        fields = ('is_active',)
        model = User

    def update(self, instance, validated_data):
        if instance.mobile == self.context['request'].user.mobile:
            raise serializers.ValidationError({"msg": "You can't perform this operation with yourself"})
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance


class UserProfileEditSerializer(serializers.ModelSerializer):
    """
    perform retrieve, update serializer for user
    """
    user_role = UserViewRoleSerializer(many=True, read_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'mobile', 'image', 'dob', 'id1', 'id2', 'address', 'is_active',
            'last_login', 'date_joined', 'user_role', 'age')
        read_only_fields = ('mobile', 'is_active', 'last_login', 'date_joined', 'user_role', 'age')
        extra_kwargs = {
            'address': {'required': False},
            'image': {'required': False},
            'mobile': {'required': False}
        }

    def get_age(self, obj):
        return (date.today() - obj.dob) // timedelta(days=365.2425)

    def validate_mobile(self, value: int) -> int:
        """
        :param value: mobile of a user
        verify user mobile number is valid or not.
        """
        valid = re.match("[6-9]{1}[0-9]{9}", str(value))
        if not valid:
            raise serializers.ValidationError("Mobile number is not in valid format")
        return value


class UserBankSerializer(serializers.ModelSerializer):
    """
    UserBank Models serializer
    """

    class Meta:
        model = UserBank
        fields = (
            'id', 'name', 'user', 'ifsc_code', 'account_number', 'created_on', 'is_delete', 'updated_on', 'created_by')
        read_only_fields = ('id', 'created_by', 'is_delete')


class UserUpiSerializer(serializers.ModelSerializer):
    """
    User Upi Models serializer
    """

    class Meta:
        model = UserUpi
        fields = ('id', 'user', 'upi', 'created_on', 'is_delete', 'updated_on', 'created_by')
        read_only_fields = ('id', 'created_by', 'is_delete')


class UserPasswordResetSerializer(serializers.ModelSerializer):
    """
       User password reset Models serializer
       """
    password = serializers.CharField(
        required=True, style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        fields = ('password',)
        model = User

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserReadSerializer(serializers.ModelSerializer):
    """
    Register new user model serializer
    """
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_age(self, obj):
        return (date.today() - obj.dob) // timedelta(days=365.2425)


class ReadUserRoleSerializer(serializers.ModelSerializer):
    """
    Role Models serializer
    """
    role = RoleSerializer()
    user = UserReadSerializer()

    class Meta:
        model = UserRoles
        fields = '__all__'
