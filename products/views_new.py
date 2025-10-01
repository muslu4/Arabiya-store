from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Count, Avg, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, ProductReview, ProductView
from . import serializers


# API views for products
class CategoryListView(generics.ListCreateAPIView):
    """API endpoint for listing and creating categories"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, and deleting a category"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductListView(generics.ListCreateAPIView):
    """API endpoint for listing and creating products"""
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'brand', 'model', 'tags']
    ordering_fields = ['price', 'created_at', 'name', 'stock_quantity']


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, and deleting a product"""
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductSearchView(APIView):
    """API endpoint for searching products"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.GET.get('q', '')
        category_id = request.GET.get('category', '')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')

        products = Product.objects.filter(is_active=True)

        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) | 
                Q(brand__icontains=query) |
                Q(model__icontains=query) |
                Q(tags__icontains=query)
            )

        if category_id:
            products = products.filter(category_id=category_id)

        if min_price:
            products = products.filter(price__gte=float(min_price))

        if max_price:
            products = products.filter(price__lte=float(max_price))

        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)


class FeaturedProductsView(APIView):
    """API endpoint for getting featured products"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_active=True, is_featured=True)
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)


class PopularProductsView(APIView):
    """API endpoint for getting popular products based on views and sales"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Get products with most views
        popular_by_views = Product.objects.annotate(
            views_count=Count('productview')
        ).filter(views_count__gt=0).order_by('-views_count')[:5]

        # Get products with most sales
        popular_by_sales = Product.objects.annotate(
            sales_count=Sum('orderitem__quantity')
        ).filter(sales_count__gt=0).order_by('-sales_count')[:5]

        # Combine results and remove duplicates
        product_ids = set()
        for product in list(popular_by_views) + list(popular_by_sales):
            product_ids.add(product.id)

        products = Product.objects.filter(id__in=product_ids)
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductRecommendationsView(APIView):
    """API endpoint for getting product recommendations based on a product"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get products from the same category
        same_category = Product.objects.filter(
            category=product.category, 
            is_active=True
        ).exclude(id=product_id)[:3]

        # Get products with similar tags
        similar_tags = Product.objects.filter(
            tags__overlap=[tag for tag in product.tags.split(',')],
            is_active=True
        ).exclude(id=product_id)[:3]

        # Combine results and remove duplicates
        product_ids = set()
        for p in list(same_category) + list(similar_tags):
            product_ids.add(p.id)

        products = Product.objects.filter(id__in=product_ids)
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductReviewListView(generics.ListCreateAPIView):
    """API endpoint for listing and creating product reviews"""
    serializer_class = serializers.ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(product=product, user=self.request.user)


class ProductStatsView(APIView):
    """API endpoint for getting product statistics"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Get basic statistics
        stats = {
            'total_products': Product.objects.count(),
            'active_products': Product.objects.filter(is_active=True).count(),
            'featured_products': Product.objects.filter(is_active=True, is_featured=True).count(),
            'low_stock_products': Product.objects.filter(stock_quantity__lt=10).count(),
            'out_of_stock_products': Product.objects.filter(stock_quantity=0).count(),
        }

        # Get average price
        avg_price = Product.objects.aggregate(Avg('price'))['price__avg']
        stats['average_price'] = round(avg_price, 2) if avg_price else 0

        # Get total value of inventory
        inventory_value = sum(product.price * product.stock_quantity for product in Product.objects.all())
        stats['inventory_value'] = round(inventory_value, 2)

        return Response(stats)


class CategoryStatsView(APIView):
    """API endpoint for getting category statistics"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Get categories with their product counts
        categories = Category.objects.annotate(
            product_count=Count('product')
        ).order_by('-product_count')

        stats = []
        for category in categories:
            stats.append({
                'id': category.id,
                'name': category.name,
                'product_count': category.product_count,
                'is_active': category.is_active,
            })

        return Response(stats)


# Admin views for custom admin functionality
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin.sites import site
from django.http import HttpResponseRedirect
from django.urls import reverse


@staff_member_required
def add_category_view(request):
    """عرض مخصص لإضافة الأقسام"""
    # الحصول على جميع الأقسام لعرضها في القائمة المنسدلة
    categories = Category.objects.all()

    if request.method == 'POST':
        # معالجة النموذج
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active') == 'on'

        # إنشاء القسم الجديد
        category = Category(
            name=name,
            parent_id=parent_id if parent_id else None,
            description=description,
            image=image,
            is_active=is_active
        )
        category.save()

        # إعادة التوجيه إلى صفحة النجاح
        return HttpResponseRedirect(reverse('admin:category-add-success', args=[category.id]))

    # عرض النموذج
    return render(request, 'admin/category_add.html', {
        'categories': categories,
        'site': site,
        'has_permission': True,
        'is_popup': False,
        'is_nav_sidebar_enabled': site.enable_nav_sidebar,
        'app_label': 'products',
        'model_name': 'category',
    })


@staff_member_required
def category_list_view(request):
    """عرض مخصص لعرض جميع الأقسام"""
    categories = Category.objects.all()

    return render(request, 'admin/category_list.html', {
        'categories': categories,
        'site': site,
        'has_permission': True,
        'is_popup': False,
        'is_nav_sidebar_enabled': site.enable_nav_sidebar,
        'app_label': 'products',
        'model_name': 'category',
    })


@staff_member_required
def category_add_success_view(request, category_id):
    """عرض صفحة النجاح بعد إضافة قسم"""
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'admin/category_add.html', {
            'error': 'القسم المحدود غير موجود',
            'categories': Category.objects.all(),
            'site': site,
            'has_permission': True,
            'is_popup': False,
            'is_nav_sidebar_enabled': site.enable_nav_sidebar,
            'app_label': 'products',
            'model_name': 'category',
        })

    return render(request, 'admin/category_add_success.html', {
        'category': category,
        'site': site,
        'has_permission': True,
        'is_popup': False,
        'is_nav_sidebar_enabled': site.enable_nav_sidebar,
        'app_label': 'products',
        'model_name': 'category',
    })
