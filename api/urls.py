from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SaleViewSet,
    PaymentMethodViewSet,
    CategoryViewSet,
    dashboard_data,
    test_api,
    today_sales_count,
)

router = DefaultRouter()
router.register(r"sales", SaleViewSet)
router.register(r"payment-methods", PaymentMethodViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard-data/", dashboard_data, name="dashboard-data"),
    path("test/", test_api, name="test-api"),
    path("today-sales-count/", today_sales_count, name="today-sales-count"),
]
