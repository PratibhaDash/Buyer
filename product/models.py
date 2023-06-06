from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    """
    Category Model
    """
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    output_per_acer_value = models.FloatField(default=1.0)
    output_per_acer_unit = models.CharField(max_length=100, default="KG")
    expected_output_days = models.IntegerField()
    expected_booking_days = models.IntegerField()
    storage_capacity_days = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class Variant(models.Model):
    """
    Variant model
    """
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_variant")
    description = models.TextField()
    payment_percentage = models.FloatField(default=30.0)
    commission = models.FloatField(default=7.0)
    price = models.FloatField(default=30.0)
    created_on = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class VariantsImage(models.Model):
    """
    image for Variants Model
    """
    image = models.ImageField()
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_image')
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']
