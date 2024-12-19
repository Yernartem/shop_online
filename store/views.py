# from django_filters import OrderingFilte
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Category, Product, Cart, CartItem, Order
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, \
    UserRegistrationSerializer

from rest_framework.filters import OrderingFilter



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    search_fields = ['name', 'category']
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name', 'price']
    ordering_fields = ['price']
    ordering = ['price']


class CartViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, is_active=True)



class CartItemViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.UpdateModelMixin,
                      viewsets.mixins.RetrieveModelMixin, viewsets.mixins.DestroyModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user,
            is_active=True,
            defaults={'is_active': True}
        )
        data = request.data.copy()
        product_id = data.get("product_id")
        existing_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += int(data.get("quantity", 1))
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=data, context={'request': request, 'cart': cart})
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.cart.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this cart item."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin, viewsets.mixins.ListModelMixin,
                   viewsets.mixins.RetrieveModelMixin):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    def create(self, request, *args, **kwargs):

        cart_id = Cart.objects.filter(
            user=self.request.user,
            is_active=True,
        ).first()

        if not cart_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(id=cart_id.id, user=request.user, is_active=True)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


        total = sum(item.product.price * item.quantity for item in cart.items.all())


        order = Order.objects.create(user=request.user, total=total)
        order.items.set(cart.items.all())


        cart.is_active = False
        cart.save()


        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def extend_schema(request, responses):
    pass


class UserRegistrationViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = UserRegistrationSerializer


    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)