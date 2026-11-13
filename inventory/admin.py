
from django.contrib import admin

from .models import (
    Category,
    Product,
    Supplier,
    Purchase,
    PurchaseItem,
    Sale,
    SaleItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'product_code', 'category',
        'purchase_price', 'selling_price',
        'quantity', 'minimum_stock'
    )
    search_fields = ('name', 'product_code')
    list_filter = ('category',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'contact_person',
        'email', 'phone', 'created_at'
    )
    search_fields = ('name', 'contact_person', 'email', 'phone')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'invoice_number', 'supplier',
        'purchase_date', 'status'
    )
    search_fields = ('invoice_number', 'supplier__name')
    list_filter = ('status', 'purchase_date')


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'purchase', 'product',
        'quantity', 'unit_price'
    )
    search_fields = ('purchase__invoice_number', 'product__name')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'invoice_number', 'customer_name',
        'sale_date', 'status'
    )
    search_fields = ('invoice_number', 'customer_name')
    list_filter = ('status', 'sale_date')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sale', 'product', 'quantity', 'unit_price'
    )
    search_fields = ('sale__invoice_number', 'product__name')
