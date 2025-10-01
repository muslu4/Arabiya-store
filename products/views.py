from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Avg, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, ProductReview, ProductView, Banner
from .serializers import (
    CategorySerializer, CategoryCreateUpdateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductReviewSerializer, ProductSearchSerializer, ProductStatsSerializer,
    CategoryStatsSerializer, PopularProductSerializer
)
from .banner_serializer import BannerSerializer


class CategoryListView(generics.ListAPIView):
    """List all active categories (supports parent filter)"""
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        qs = Category.objects.filter(is_active=True).order_by('name')
        parent_id = self.request.query_params.get('parent')
        if parent_id is not None:
            if parent_id == 'null':
                qs = qs.filter(parent__isnull=True)
            else:
                qs = qs.filter(parent_id=parent_id)
        return qs


class CategoryCreateView(generics.CreateAPIView):
    """Create new category (Admin only)"""
    serializer_class = CategoryCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بإنشاء أقسام جديدة")
        serializer.save()


class CategoryUpdateView(generics.UpdateAPIView):
    """Update category (Admin only)"""
    serializer_class = CategoryCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بتعديل الأقسام")
        return Category.objects.all()


class CategoryDeleteView(generics.DestroyAPIView):
    """Delete category (Admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بحذف الأقسام")
        return Category.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        if category.products.exists():
            return Response({
                'error': 'لا يمكن حذف قسم يحتوي على منتجات'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        category.delete()
        return Response({
            'message': 'تم حذف القسم بنجاح'
        }, status=status.HTTP_200_OK)


class ProductListView(generics.ListAPIView):
    """List all active products with filtering and pagination"""
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by featured
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by stock status
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock_quantity__gt=0)
        
        # Filter by brand
        brand = self.request.query_params.get('brand')
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """Get product details"""
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category')
    
    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        
        # Track product view
        self.track_product_view(product, request)
        
        serializer = self.get_serializer(product)
        return Response(serializer.data)
    
    def track_product_view(self, product, request):
        """Track product view for analytics"""
        try:
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Get user agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Create view record
            ProductView.objects.create(
                product=product,
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip,
                user_agent=user_agent
            )
        except Exception as e:
            # Don't fail the request if view tracking fails
            print(f"Failed to track product view: {e}")


class ProductCreateView(generics.CreateAPIView):
    """Create new product (Admin only)"""
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بإنشاء منتجات جديدة")
        serializer.save()


class ProductUpdateView(generics.UpdateAPIView):
    """Update product (Admin only)"""
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بتعديل المنتجات")
        return Product.objects.all()


class ProductDeleteView(generics.DestroyAPIView):
    """Delete product (Admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بحذف المنتجات")
        return Product.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({
            'message': 'تم حذف المنتج بنجاح'
        }, status=status.HTTP_200_OK)


class ProductSearchView(generics.ListAPIView):
    """Search products by name, description, or tags"""
    serializer_class = ProductSearchSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return Product.objects.none()
        
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query) |
            Q(brand__icontains=query),
            is_active=True
        ).select_related('category')[:20]  # Limit to 20 results


class ProductReviewListView(generics.ListAPIView):
    """List product reviews"""
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(
            product_id=product_id,
            is_approved=True
        ).select_related('user').order_by('-created_at')


class ProductReviewCreateView(generics.CreateAPIView):
    """Create product review"""
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check if user already reviewed this product
        if ProductReview.objects.filter(
            product=product,
            user=self.request.user
        ).exists():
            raise serializers.ValidationError("لقد قمت بتقييم هذا المنتج من قبل")
        
        serializer.save(product=product)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """Get featured products"""
    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category')[:8]  # Limit to 8 featured products
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_products(request):
    """Get popular products based on views"""
    # Get products with most views in the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    popular_products = Product.objects.filter(
        is_active=True,
        views__viewed_at__gte=thirty_days_ago
    ).annotate(
        views_count=Count('views')
    ).order_by('-views_count')[:8]
    
    serializer = PopularProductSerializer(popular_products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def product_stats(request):
    """Get product statistics (Admin only)"""
    if not request.user.is_admin:
        return Response({
            'error': 'غير مصرح لك بالوصول لهذه البيانات'
        }, status=status.HTTP_403_FORBIDDEN)
    
    stats = {
        'total_products': Product.objects.count(),
        'active_products': Product.objects.filter(is_active=True).count(),
        'featured_products': Product.objects.filter(is_featured=True).count(),
        'out_of_stock_products': Product.objects.filter(stock_quantity=0).count(),
        'low_stock_products': Product.objects.filter(
            stock_quantity__gt=0,
            stock_quantity__lte=models.F('low_stock_threshold')
        ).count(),
        'total_categories': Category.objects.count(),
        'total_reviews': ProductReview.objects.count(),
    }
    
    serializer = ProductStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def category_stats(request):
    """Get category statistics (Admin only)"""
    if not request.user.is_admin:
        return Response({
            'error': 'غير مصرح لك بالوصول لهذه البيانات'
        }, status=status.HTTP_403_FORBIDDEN)
    
    categories = Category.objects.annotate(
        products_count=Count('products'),
        active_products_count=Count('products', filter=Q(products__is_active=True)),
        total_stock=Sum('products__stock_quantity')
    ).values(
        'name', 'products_count', 'active_products_count', 'total_stock'
    )
    
    stats = []
    for category in categories:
        stats.append({
            'category_name': category['name'],
            'products_count': category['products_count'] or 0,
            'active_products_count': category['active_products_count'] or 0,
            'total_stock': category['total_stock'] or 0,
        })
    
    serializer = CategoryStatsSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_recommendations(request, product_id):
    """Get product recommendations based on category and price range"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response({
            'error': 'المنتج غير موجود'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get similar products from same category with similar price range
    price_range = product.price * 0.3  # 30% price range
    min_price = product.price - price_range
    max_price = product.price + price_range
    
    recommendations = Product.objects.filter(
        category=product.category,
        is_active=True,
        price__gte=min_price,
        price__lte=max_price
    ).exclude(id=product.id)[:6]
    
    serializer = ProductListSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def banner_list(request):
    """Get all active banners for homepage slider"""
    banners = Banner.objects.filter(
        is_active=True
    ).order_by('display_order')

    result = []
    for banner in banners:
        result.append({
            'id': banner.id,
            'title': banner.title,
            'description': banner.description,
            'image': banner.image,
            'link': banner.get_link(),
            'display_order': banner.display_order
        })

    return Response(result)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .imgbb import upload_image_file, ImgBBError

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def upload_image_to_imgbb(request):
    """
    Admin view to upload an image to ImgBB and return the URL.
    """
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image file found'}, status=400)

    file_obj = request.FILES['image']
    
    try:
        image_url = upload_image_file(file_obj, name_prefix="product_image")
        if image_url:
            return JsonResponse({'url': image_url})
        else:
            return JsonResponse({'error': 'Failed to get image URL from ImgBB response'}, status=500)
    except ImgBBError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
