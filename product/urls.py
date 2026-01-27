from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    CompanyViewSet,
    UnitViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'companys', CompanyViewSet, basename='companys')
router.register(r'units', UnitViewSet, basename='units')
router.register(r'categorys', CategoryViewSet, basename='categorys')

urlpatterns = [
    path('', include(router.urls)),
]
