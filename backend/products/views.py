from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import Product, Category, Banner
from .serializers import ProductSerializer, CategorySerializer, BannerSerializer
from django.conf import settings
import requests

@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_image_to_imgbb(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image file provided'}, status=400)

    image_file = request.FILES['image']
    api_key = settings.IMGBB_API_KEY

    if not api_key:
        return Response({'error': 'ImgBB API key is not configured'}, status=500)

    try:
        response = requests.post(
            'https://api.imgbb.com/1/upload',
            params={'key': api_key},
            files={'image': image_file}
        )
        response.raise_for_status()
        result = response.json()

        if result.get('data') and result['data'].get('url'):
            return Response({'url': result['data']['url']})
        else:
            error_message = result.get('error', {}).get('message', 'Unknown error from ImgBB')
            return Response({'error': error_message}, status=500)

    except requests.exceptions.RequestException as e:
        return Response({'error': f'Failed to connect to ImgBB: {e}'}, status=500)
    except Exception as e:
        return Response({'error': f'An unexpected error occurred: {e}'}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    """
    قائمة جميع المنتجات
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, pk):
    """
    تفاصيل منتج محدد
    """
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'المنتج غير موجود'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    """
    قائمة جميع الفئات
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products(request):
    """
    قائمة المنتجات المميزة
    """
    products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    """
    البحث عن المنتجات
    """
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def banner_list(request):
    """
    قائمة جميع البانرات
    """
    banners = Banner.objects.filter(is_active=True)
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

