from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from farm_app.models import Farms
from product.models import Variant, Product, Category

User = get_user_model()


class FarmPurchase(models.Model):
    """
    Farms Purchase model to store farm details and buyer details
    """
    farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='farm_purchase')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='farm_purchase_category')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='farm_purchase_product')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='farm_purchase_variant')
    purchased_value = models.FloatField(default=1.0)
    purchased_unit = models.CharField(max_length=100, default="KG")
    price = models.FloatField()
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    purchased_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_purchased_by')

    def __str__(self):
        return self.purchased_by.email + " " + self.farm.name + " " + self.product.name

    class Meta:
        ordering = ['-created_on']
