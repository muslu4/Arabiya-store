from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('featured/', views.featured_products, name='featured_products'),
    path('search/', views.search_products, name='search_products'),

    path('upload-image/', views.upload_image_to_imgbb, name='upload_image'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/products/', views.products_by_category, name='products_by_category'),
    
    # Banners
    path('banners/', views.banner_list, name='banner_list'),
]

