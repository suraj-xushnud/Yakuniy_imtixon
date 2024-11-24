from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')  # Admin panelda ko'rsatiladigan ustunlar
    search_fields = ('name', 'description')  # Qidiruv maydoni
    list_filter = ('name',)  # Filtrlash imkoniyati


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'current_price', 'old_price')
    list_filter = ('category',)
    search_fields = ('name', 'description')
