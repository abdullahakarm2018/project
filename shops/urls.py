from django.urls import path
from shops.views import ProductShopCreateAPIView, ProductShopDeleteAPIView, ProductShopUpdateAPIView, ShopCategoriesAPIView, ShopProductsAPIView
from users import views
urlpatterns = [
    path('shop-products/', ShopProductsAPIView.as_view(), name='shop-products'),
    path('shop-categories/', ShopCategoriesAPIView.as_view(), name='shop-products'),
    path('shop-product-add/', ProductShopCreateAPIView.as_view(), name='add-product-shop'),
    path('shop-product-update/<int:pk>/', ProductShopUpdateAPIView.as_view(), name='update-product-shop'),
    path('shop-product-delete/<int:pk>/', ProductShopDeleteAPIView.as_view(), name='delete-product-shop'),




    
]