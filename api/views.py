from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import datetime, timedelta
from .serializers import (
    SaleSerializer,
    PaymentMethodSerializer,
    CategorySerializer,
    ProductSerializer,
)
from dashboard.models import Sale, PaymentMethod, Category, Product
import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
@login_required
def test_api(request):
    """Simple test endpoint to check if API is working"""
    try:
        categories_count = Category.objects.count()
        payment_methods_count = PaymentMethod.objects.count()
        products_count = Product.objects.count()
        sales_count = Sale.objects.count()

        return Response(
            {
                "status": "API is working",
                "categories_count": categories_count,
                "payment_methods_count": payment_methods_count,
                "products_count": products_count,
                "sales_count": sales_count,
            }
        )
    except Exception as e:
        logger.error(f"Test API error: {str(e)}")
        return Response(
            {"error": f"API test failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@login_required
def today_sales_count(request):
    """Get today's sales count and total value"""
    try:
        # Use Bangladesh timezone
        from django.utils import timezone
        from pytz import timezone as pytz_timezone

        # Get current time in Bangladesh timezone
        bd_timezone = pytz_timezone("Asia/Dhaka")
        today = timezone.now().astimezone(bd_timezone).date()
        print(f"Today's date in Bangladesh timezone: {today}")

        # Get today's sales
        today_sales = Sale.objects.filter(created_at__date=today)
        today_count = today_sales.count()
        today_total = today_sales.aggregate(total=Sum("total_amount"))["total"] or 0

        data = {
            "today_count": today_count,
            "today_total": float(today_total),
            "date": today.isoformat(),
        }

        logger.info(f"Today's sales data: {data}")
        return Response(data)

    except Exception as e:
        logger.error(f"Error in today_sales_count: {str(e)}")
        return Response(
            {"error": f"Failed to load today's sales count: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination for products

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Get products filtered by category"""
        category_id = request.query_params.get("category_id")
        if category_id:
            products = self.queryset.filter(category_id=category_id)
        else:
            products = self.queryset
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def stockable(self, request):
        """Get only stockable products"""
        products = self.queryset.filter(product_type="stockable")
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def non_stockable(self, request):
        """Get only non-stockable products"""
        products = self.queryset.filter(product_type="non_stockable")
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """Get products with low stock"""
        products = self.queryset.filter(
            product_type="stockable", stock_quantity__lte=models.F("min_stock_level")
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def quick_actions(self, request):
        """Get products marked as quick actions"""
        products = self.queryset.filter(is_quick_action=True, is_active=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Received sale data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Get the product and check stock availability
                product_id = request.data.get("product")
                quantity = int(request.data.get("quantity", 0))

                try:
                    product = Product.objects.get(id=product_id)

                    # Check stock for stockable products
                    if product.product_type == "stockable":
                        if product.stock_quantity <= 0:
                            return Response(
                                {
                                    "error": f"Product '{product.name}' is out of stock! Please restock before selling."
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                        if quantity > product.stock_quantity:
                            return Response(
                                {
                                    "error": f"Insufficient stock for '{product.name}'! Available: {product.stock_quantity}, Requested: {quantity}"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                except Product.DoesNotExist:
                    return Response(
                        {"error": "Product not found"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                sale = serializer.save()
                logger.info(f"Sale created successfully: {sale}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating sale: {str(e)}")
            return Response(
                {"error": f"Failed to create sale: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def today(self, request):
        # Use Bangladesh timezone
        from django.utils import timezone
        from pytz import timezone as pytz_timezone

        # Get current time in Bangladesh timezone
        bd_timezone = pytz_timezone("Asia/Dhaka")
        today = timezone.now().astimezone(bd_timezone).date()

        sales = Sale.objects.filter(created_at__date=today)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        sales = Sale.objects.all()[:10]
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def monthly(self, request):
        # Use Bangladesh timezone
        from django.utils import timezone
        from pytz import timezone as pytz_timezone

        # Get current time in Bangladesh timezone
        bd_timezone = pytz_timezone("Asia/Dhaka")
        today = timezone.now().astimezone(bd_timezone).date()
        start_of_month = today.replace(day=1)

        sales = Sale.objects.filter(created_at__date__gte=start_of_month)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@login_required
def dashboard_data(request):
    try:
        # Use Bangladesh timezone
        from django.utils import timezone
        from pytz import timezone as pytz_timezone

        # Get current time in Bangladesh timezone
        bd_timezone = pytz_timezone("Asia/Dhaka")
        today = timezone.now().astimezone(bd_timezone).date()

        # Today's sales
        today_sales = Sale.objects.filter(created_at__date=today)
        today_total = today_sales.aggregate(total=Sum("total_amount"))["total"] or 0
        today_count = today_sales.count()

        # Recent sales (last 5)
        recent_sales = Sale.objects.all()[:5]

        # Monthly total
        start_of_month = today.replace(day=1)
        monthly_sales = Sale.objects.filter(created_at__date__gte=start_of_month)
        monthly_total = monthly_sales.aggregate(total=Sum("total_amount"))["total"] or 0

        # Category breakdown (using product category)
        category_breakdown = (
            Sale.objects.filter(created_at__date=today)
            .values("product__category__name")
            .annotate(total=Sum("total_amount"), count=Count("id"))
            .order_by("-total")
        )

        # Payment method breakdown
        payment_breakdown = (
            Sale.objects.filter(created_at__date=today)
            .values("payment_method__name")
            .annotate(total=Sum("total_amount"), count=Count("id"))
            .order_by("-total")
        )

        data = {
            "today_total": float(today_total),
            "today_count": today_count,
            "monthly_total": float(monthly_total),
            "recent_sales": SaleSerializer(recent_sales, many=True).data,
            "category_breakdown": list(category_breakdown),
            "payment_breakdown": list(payment_breakdown),
        }

        logger.info(f"Dashboard data: {data}")
        return Response(data)

    except Exception as e:
        logger.error(f"Error in dashboard_data: {str(e)}")
        return Response(
            {"error": f"Failed to load dashboard data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
