from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)  # Поле для поиска
    ordering = ('name',)  # Сортировка


# Регистрация модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')  # Отображаемые поля
    list_filter = ('category',)  # Фильтр по категории
    search_fields = ('name',)  # Поле для поиска
    ordering = ('category', 'name')  # Сортировка


# Регистрация модели CartItem (позиция корзины)
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Количество пустых форм для добавления новых позиций


# Регистрация модели Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')  # Отображаемые поля
    ordering = ('-created_at',)  # Сортировка по дате создания
    inlines = [CartItemInline]  # Вложенные элементы для управления CartItem


# Регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'created_at')  # Отображаемые поля
    list_filter = ('user', 'created_at')  # Фильтры по пользователю и дате создания
    search_fields = ('user__username', 'total')  # Поле для поиска
    ordering = ('-created_at',)  # Сортировка по дате создания
    filter_horizontal = ('items',)  # Для удобного управления ManyToManyField
