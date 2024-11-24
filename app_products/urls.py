from django.urls import path
from .views import categories_home, category_products, product_search

urlpatterns = [
    path('', categories_home, name='categories_home'),  # Kategoriyalar bosh sahifasi
    path('<int:category_id>/', category_products, name='category_products'),  # Mahsulotlar uchun yo'l
    path('search/', product_search, name='product_search'),

]
