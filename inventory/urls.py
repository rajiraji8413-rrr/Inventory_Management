
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    SupplierViewSet,
    PurchaseViewSet,
    PurchaseItemViewSet,
    SaleViewSet,
    SaleItemViewSet,
    StockViewSet
)


# Create API Router
router = DefaultRouter()


# Category API
router.register(
    'categories',
    CategoryViewSet,
    basename='category'
)


# Product API
router.register(
    'products',
    ProductViewSet,
    basename='product'
)


# Supplier API
router.register(
    'suppliers',
    SupplierViewSet,
    basename='supplier'
)


# Purchase API
router.register(
    'purchases',
    PurchaseViewSet,
    basename='purchase'
)


# Purchase Item API
router.register(
    'purchase-items',
    PurchaseItemViewSet,
    basename='purchase-item'
)


# Sales API
router.register(
    'sales',
    SaleViewSet,
    basename='sale'
)


# Sale Item API
router.register(
    'sale-items',
    SaleItemViewSet,
    basename='sale-item'
)


# Stock API
router.register(
    'stock',
    StockViewSet,
    basename='stock'
)


urlpatterns = [
    path('api/', include(router.urls)),
]
