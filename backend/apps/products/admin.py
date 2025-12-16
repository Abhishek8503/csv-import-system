from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "is_active", "created_at")
    search_fields = ("sku", "name")
    list_filter = ("is_active",)
