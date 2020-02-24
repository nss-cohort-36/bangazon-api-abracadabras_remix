from django.db import models
from .orders import Order
from .products import Product

class OrderProduct(models.Model):
    """
        This creates instances of OrderProduct
        - RHC
    """

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)


    class Meta:
        verbose_name = ("order_product")
        verbose_plural = ("order_products")

    def __str__(self):
        return f'Order: {self.order.id}\n Product/s: ${self.product.name}' 