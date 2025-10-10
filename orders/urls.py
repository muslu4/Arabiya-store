from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart management
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/items/<int:item_id>/update/', views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/items/<int:item_id>/remove/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/clear/', views.ClearCartView.as_view(), name='clear-cart'),
    
    # Orders
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),
    path('<int:order_id>/cancel/', views.OrderCancelView.as_view(), name='order-cancel'),
    path('<int:order_id>/history/', views.order_status_history, name='order-history'),
    
    # Admin endpoints
    path('admin/all/', views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:pk>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('admin/<int:order_id>/status/', views.AdminOrderStatusUpdateView.as_view(), name='admin-order-status-update'),
    path('admin/stats/', views.order_stats, name='order-stats'),
    
    # Utilities
    path('shipping-cost/', views.shipping_cost_calculator, name='shipping-cost'),
]