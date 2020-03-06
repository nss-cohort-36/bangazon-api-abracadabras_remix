from django.db import models
from .customer import Customer
from .payment_type import PaymentType
from .product import Product

class Order(models.Model):

    """

    This class creates instances of the order.

    Author:
        Shawna Chatfield

    """

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ("created_at", )
        verbose_name = ("order")
        verbose_name_plural = ("orders")


    def __str__(self):
        return f'Order Number: {self.id} Customer: {self.customer.user.first_name} {self.customer.user.last_name}'