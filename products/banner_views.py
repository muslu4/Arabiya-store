from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Banner
from .banner_serializer import BannerSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def banner_list(request):
    """Get all active banners for homepage slider"""
    banners = Banner.objects.filter(
        is_active=True
    ).order_by('display_order')

    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_sample_banners(request):
    """Create sample banners (Admin only)"""
    if not request.user.is_admin:
        return Response({
            'error': 'غير مصرح لك بإضافة إعلانات'
        }, status=status.HTTP_403_FORBIDDEN)

    # Sample banner data
    banner_data = [
        {
            'title': 'تخفيضات الصيف',
            'description': 'خصم يصل إلى 50% على جميع منتجات الصيف',
            'image': 'https://i.ibb.co/8X0Q2vN/summer-sale.jpg',
            'link_url': 'https://example.com/summer-sale',
            'is_active': True,
            'display_order': 1
        },
        {
            'title': 'منتجات جديدة',
            'description': 'استكشف أحدث منتجاتنا المضافة',
            'image': 'https://i.ibb.co/3dX0qQJ/new-products.jpg',
            'link_url': 'https://example.com/new-products',
            'is_active': True,
            'display_order': 2
        },
        {
            'title': 'عروض الأسبوع',
            'description': 'عروض خاصة لهذا الأسبوع فقط',
            'image': 'https://i.ibb.co/2Z7QfVf/weekly-offers.jpg',
            'link_url': 'https://example.com/weekly-offers',
            'is_active': True,
            'display_order': 3
        },
        {
            'title': 'توصيل مجاني',
            'description': 'توصيل مجاني لجميع الطلبات فوق 100 ريال',
            'image': 'https://i.ibb.co/6WZqQ0T/free-shipping.jpg',
            'link_url': 'https://example.com/free-shipping',
            'is_active': True,
            'display_order': 4
        },
        {
            'title': 'مجموعة الإلكترونيات',
            'description': 'أحدث الأجهزة الإلكترونية بأسعار مميزة',
            'image': 'https://i.ibb.co/Zf3Q3rN/electronics.jpg',
            'link_url': 'https://example.com/electronics',
            'is_active': True,
            'display_order': 5
        }
    ]

    created_banners = []

    for data in banner_data:
        banner, created = Banner.objects.get_or_create(
            title=data['title'],
            defaults=data
        )
        if created:
            created_banners.append(banner)

    serializer = BannerSerializer(created_banners, many=True)
    return Response({
        'message': f'تم إنشاء {len(created_banners)} إعلان بنجاح',
        'banners': serializer.data
    }, status=status.HTTP_201_CREATED)
