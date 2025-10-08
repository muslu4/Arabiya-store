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
        # Use base64 encoding for the image
        import base64
        import io
        
        # Read image file and encode to base64
        image_data = image_file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare payload
        payload = {
            'key': api_key,
            'image': encoded_image,
            'name': image_file.name,
            'expiration': 3600  # 1 hour
        }
        
        # Make request
        response = requests.post(
            'https://api.imgbb.com/1/upload',
            data=payload
        )
        
        # Check response
        print(f"ImgBB response status: {response.status_code}")
        print(f"ImgBB response: {response.text}")
        
        response.raise_for_status()
        result = response.json()

        if result.get('data') and result['data'].get('url'):
            return Response({
                'url': result['data']['url'],
                'thumb_url': result['data'].get('thumb', {}).get('url'),
                'delete_url': result['data'].get('delete_url')
            })
        else:
            error_message = result.get('error', {}).get('message', 'Unknown error from ImgBB')
            return Response({'error': error_message}, status=500)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response body: {e.response.text if e.response else 'No response'}")
        return Response({'error': f'HTTP error from ImgBB: {e}'}, status=e.response.status_code if e.response else 500)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return Response({'error': f'Failed to connect to ImgBB: {e}'}, status=500)
    except Exception as e:
        print(f"Unexpected Error: {e}")
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
    print(f"Found {banners.count()} active banners")
    for banner in banners:
        print(f"Banner: {banner.title}, Product: {banner.product}, Image URL: {banner.get_image_url()}")
    serializer = BannerSerializer(banners, many=True, context={'request': request})
    print(f"Serialized banners data: {serializer.data}")
    return Response(serializer.data)

