from django.db import models
from django.db.models.functions import Lower

# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(Lower("sku"), name="idx_product_sku_lower"),
        ]

        constraints = [
            models.UniqueConstraint(
                Lower("sku"),
                name="unique_product_sku_case_insensitive",
            )
        ]
    
    def __str__(self):
        return f"{self.sku} - {self.name}"