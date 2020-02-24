from django.db import models

class ProductType(models.Model):
    """
    This is a class to create a blueprint for product type Object to be instantiated.

    Warning: This is a Jeremiah Bell Disaster
    """

    name = models.CharField(max_length=55)

    class Meta:
        verbose_name = ("product_type")
        verbose_name_plural = ("product_types")

    def __str__(self):
        return self.name