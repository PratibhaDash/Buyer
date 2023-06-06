import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, mobile, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not mobile:
            raise ValueError(_('The mobile must be set'))
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(mobile, password, **extra_fields)


# Create your models here
class CustomUser(AbstractUser):
    """
    Create and save a User Details.
    """
    username = None
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=15, unique=True)
    image = models.ImageField()
    dob = models.DateField(default="2021-01-01")
    address = models.TextField(null=True)
    id1 = models.CharField(max_length=250, null=True)
    id2 = models.CharField(max_length=250, null=True)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, verbose_name='active')
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile

    class Meta:
        ordering = ['-date_joined']


class Role(models.Model):
    """
    Role creation
    """
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']


class UserRoles(models.Model):
    """
    Role Model
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role')
    status = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role',)
        ordering = ['-created_on']


class UserBank(models.Model):
    """
    user bank account model
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_bank')
    ifsc_code = models.CharField(max_length=50, default="SBIN0000000")
    account_number = models.IntegerField()
    name = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['-created_on']


class UserUpi(models.Model):
    """
    user upi model
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_upi')
    upi = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['-created_on']
