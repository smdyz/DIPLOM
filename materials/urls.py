from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CategoryViewSet, ProductCreateAPIView, ProductListAPIView, ProductUpdateAPIView, \
    ProductDeleteAPIView, ProductRetrieveAPIView, SubscriptionAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('product/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('product/', ProductListAPIView.as_view(), name='products-list'),
    path('product/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product'),
    path('product/update/<int:pk>/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('subscription/', SubscriptionAPIView.as_view(), name='sub'),
] + router.urls
