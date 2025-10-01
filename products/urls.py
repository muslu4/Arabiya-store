from django.urls import path
from . import views
from . import banner_views

app_name = 'products'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Products
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('upload-image/', views.upload_image_to_imgbb, name='product-upload-image'),
    
    # Product search and filtering
    path('search/', views.ProductSearchView.as_view(), name='product-search'),
    path('featured/', views.featured_products, name='featured-products'),
    path('popular/', views.popular_products, name='popular-products'),
    path('<int:product_id>/recommendations/', views.product_recommendations, name='product-recommendations'),
    
    # Product reviews
    path('<int:product_id>/reviews/', views.ProductReviewListView.as_view(), name='product-reviews'),
    path('<int:product_id>/reviews/create/', views.ProductReviewCreateView.as_view(), name='product-review-create'),
    
    # Banners
    path('banners/', banner_views.banner_list, name='banner-list'),
    path('banners/create-samples/', banner_views.create_sample_banners, name='create-sample-banners'),
    
    # Statistics (Admin only)
    path('stats/', views.product_stats, name='product-stats'),
    path('categories/stats/', views.category_stats, name='category-stats'),
]