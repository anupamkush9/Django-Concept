from django.urls import path
from . import views

urlpatterns = [
 path('checkout_home/', views.home, name='checkout_home'),
 path('create-checkout-session/<str:product_id>', views.create_checkout_session, name='checkout'),
 path('success/', views.success,name='success'),
 path('cancel/', views.cancel,name='cancel'),
 path('webhooks/', views.webhook,name='cancel'),
]
