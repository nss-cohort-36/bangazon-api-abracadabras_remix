from .customer import Customer
from django.db import models

class PaymentType(models.Model):
    """ This model is for payment types. Created by Erin Polley, Esq."""

    merchant_name = models.CharField(max_length=50)
    acct_number = models.CharField(max_length=15)
    expiration_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("payment_type")
        verbose_name_plural = ("payment_types")

    def __str__(self):
        return f'Merchant Name--{self.merchant_name}. Account Number--{self.acct_number}. Expiration Date--{self.expiration_date}'
