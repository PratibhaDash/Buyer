import datetime
from django.contrib.auth import get_user_model
from django.db import models
from product.models import Variant, Product, Category

User = get_user_model()


# Create your models here.
class Farms(models.Model):
    """
    Farms creation
    """
    name = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=40)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pin = models.IntegerField()
    land_value = models.FloatField(default=1.0)
    land_unit = models.CharField(max_length=100, default="ACRE")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='farm_category')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='farm_product')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='farm_variant')
    minimum_sell_value = models.FloatField(default=1.0)
    minimum_sell_unit = models.CharField(max_length=100, default="KG")
    price = models.FloatField()
    expected_harvesting_date = models.DateField()
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):

        if self.pk is not None:  # Adding of a new instance
            farms = Farms.objects.get(id=self.pk)
            previous_price = farms.price
            if previous_price != self.price:
                FarmLogs.objects.create(farm=self, previous_price=previous_price, desc="Farm price updated",
                                        updated_price=self.price, created_by=self.created_by,
                                        created_on=datetime.datetime.now)
            super(Farms, self).save(*args, **kwargs)
        else:
            instance = super(Farms, self).save(*args, **kwargs)
            FarmLogs.objects.create(farm=instance, previous_price=0.0, desc="Farm created",
                                    updated_price=self.price, created_by=self.created_by,
                                    created_on=datetime.datetime.now)


class FarmLogs(models.Model):
    farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='farm_log')
    previous_price = models.FloatField()
    updated_price = models.FloatField()
    desc = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.farm.name

    class Meta:
        ordering = ['-created_on']


class FarmsImage(models.Model):
    """
    image for Farms Model
    """
    image = models.ImageField()
    farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='farm_image')
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']


farm_stages_status = (('IN-PROGRESS', 'IN-PROGRESS'), ('REJECTED', 'REJECTED'), ('ACCEPTED', 'ACCEPTED'))


class StagesMaster(models.Model):
    """
    Stage Model
    """
    stage_no = models.FloatField()
    name = models.CharField(max_length=150)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stage_product')
    payment_percentage = models.FloatField(default=0)
    expected_days = models.FloatField()
    description = models.TextField(default="Please upload clear image")
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stage_created_by')

    class Meta:
        unique_together = ('stage_no', 'product',)
        ordering = ['stage_no']


class FarmStage(models.Model):
    """
    Farms Stage Model
    """
    stage = models.ForeignKey(StagesMaster, on_delete=models.CASCADE, related_name='stage')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='farm_stage_product')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='farm_stage_variant')
    farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='farm_stage')
    status = models.CharField(max_length=50, choices=farm_stages_status, default='IN-PROGRESS')
    message = models.TextField(default='NOT ADDED')
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_stage_created_by')

    class Meta:
        ordering = ['-created_on']


class FarmStagesImage(models.Model):
    """
    image for Farms Stages Model
    """
    image = models.ImageField()
    farm_stage = models.ForeignKey(FarmStage, on_delete=models.CASCADE, related_name='farm_stage_image')
    description = models.TextField(default="image")
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']


class VariantCommission(models.Model):
    """
      model to store Commission on Variant
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='variant_commission_category')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant_commission_product')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variant_Commission_variant')
    percentage = models.FloatField(default=1.0)
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.variant.name

    class Meta:
        ordering = ['-created_on']


class FarmerPayment(models.Model):
    """
    Farmer payment Model
    """
    stage = models.ForeignKey(StagesMaster, on_delete=models.CASCADE, related_name='payment_stage')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payment_stage_product')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='payment_stage_variant')
    farm = models.ForeignKey(Farms, on_delete=models.CASCADE, related_name='payment_farm')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payment')
    image = models.ImageField()
    amount = models.FloatField()
    account = models.CharField(max_length=100)
    payment_on = models.DateTimeField()
    is_delete = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farm_payment_created_by')

    class Meta:
        ordering = ['-created_on']
