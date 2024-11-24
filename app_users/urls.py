from django.urls import path
from app_users.views import register, user_login, user_logout, account_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),  # Logout uchun URL
    path('account/', account_view, name='account')
]
