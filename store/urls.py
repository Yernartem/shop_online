from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet, UserRegistrationViewSet, \
     UserViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'register', UserRegistrationViewSet, basename='user-registration')
router.register(r'user',UserViewSet,basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
