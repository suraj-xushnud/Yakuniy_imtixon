from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_products.urls')),  # app_products yo'nalishlarini ulash
    path('users/', include('app_users.urls')),  # Ro'yxatdan o'tish va login uchun
    path('cart/', include('app_carts.urls')),  # Cart ilovasini to'g'ri bog'lash
    path('social-auth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
