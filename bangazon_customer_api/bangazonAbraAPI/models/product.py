from django.db import models
from .customers import Customer
from .product_type import ProductType

class Product(models.Model):
    """
    This is a blueprint for instance of Product Object.

    associated keys: customer, product_type

    Warning: This is a Jeremiah Bell Disaster
    """

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="customers")
    product_type = models.ForeignKey(
        ProductType, on_delete=models.DO_NOTHING, related_name="product_types"
    )

class Meta:
    ordering = ("-created.at",)
    verbose_name = ("product")
    verbose_name_plural = ("products")

def __str__(self):
    return f'{self.name} costs ${self.price} user who posted is {self.customer.user.first_name} {self.customer.user.last_name}.'
