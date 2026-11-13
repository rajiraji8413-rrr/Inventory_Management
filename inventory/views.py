
from django.db.models import F
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import ValidationError

from .models import (
    Category,
    Product,
    Supplier,
    Purchase,
    PurchaseItem,
    Sale,
    SaleItem
)

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    SupplierSerializer,
    PurchaseSerializer,
    PurchaseItemSerializer,
    SaleSerializer,
    SaleItemSerializer
)


# =====================================
# CATEGORY API
# =====================================

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# =====================================
# PRODUCT API
# =====================================

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ['name', 'product_code']

    ordering_fields = [
        'name',
        'purchase_price',
        'selling_price',
        'quantity',
        'created_at'
    ]

    ordering = ['name']

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()

        category_id = self.request.query_params.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


# =====================================
# SUPPLIER API
# =====================================

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


# =====================================
# PURCHASE API
# =====================================

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.select_related('supplier').all()
    serializer_class = PurchaseSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['invoice_number', 'supplier__name']
    ordering_fields = ['purchase_date', 'created_at']
    ordering = ['-purchase_date']

    @transaction.atomic
    def perform_update(self, serializer):
        old_status = serializer.instance.status
        purchase = serializer.save()

        if old_status != 'Received' and purchase.status == 'Received':

            items = purchase.items.all()

            quantities = {}

            for item in items:
                quantities[item.product_id] = (
                    quantities.get(item.product_id, 0) + item.quantity
                )

            products = Product.objects.select_for_update().filter(
                id__in=sorted(quantities.keys())
            )

            for product in products:
                product.quantity += quantities[product.id]
                product.save(update_fields=['quantity'])


# =====================================
# PURCHASE ITEM API
# =====================================

class PurchaseItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseItem.objects.select_related(
        'purchase', 'product'
    ).all()

    serializer_class = PurchaseItemSerializer


# =====================================
# SALES API
# =====================================

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['invoice_number', 'customer_name']
    ordering_fields = ['sale_date', 'created_at']
    ordering = ['-sale_date']

    @transaction.atomic
    def perform_update(self, serializer):

        old_status = serializer.instance.status
        sale = serializer.save()

        # Reduce stock only when sale becomes Completed
        if old_status != 'Completed' and sale.status == 'Completed':

            items = sale.items.all()

            quantities = {}

            for item in items:
                quantities[item.product_id] = (
                    quantities.get(item.product_id, 0) + item.quantity
                )

            products = Product.objects.select_for_update().filter(
                id__in=sorted(quantities.keys())
            )

            product_list = list(products)

            if len(product_list) != len(quantities):
                raise ValidationError("One or more products were not found.")

            # Check stock before reducing it
            for product in product_list:
                required_quantity = quantities[product.id]

                if product.quantity < required_quantity:
                    raise ValidationError({
                        'stock': (
                            f'Insufficient stock for {product.name}. '
                            f'Available: {product.quantity}, '
                            f'Required: {required_quantity}.'
                        )
                    })

            # Reduce stock
            for product in product_list:
                product.quantity -= quantities[product.id]
                product.save(update_fields=['quantity'])


# =====================================
# SALE ITEM API
# =====================================

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.select_related(
        'sale', 'product'
    ).all()

    serializer_class = SaleItemSerializer

# =====================================
# STOCK MANAGEMENT API
# =====================================

class StockViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):

        products = Product.objects.filter(
            quantity__lte=F('minimum_stock')
        ).select_related('category')

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response({
            'total_low_stock_products': products.count(),
            'products': serializer.data
        })
