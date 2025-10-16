
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal

from .models_coupons import Coupon, CouponUsage
from .serializers_coupons import CouponSerializer, CouponUsageSerializer, CouponApplySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_coupons(request):
    """
    الحصول على قائمة الكوبونات المتاحة للمستخدم
    """
    now = timezone.now()
    # الحصول على الكوبونات النشطة والصالحة حاليًا
    coupons = Coupon.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    )

    # استبعاد الكوبونات التي استخدمها المستخدم بالفعل
    used_coupons = CouponUsage.objects.filter(user=request.user).values_list('coupon_id', flat=True)
    coupons = coupons.exclude(id__in=used_coupons)

    serializer = CouponSerializer(coupons, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([])  # السماح بالطلبات بدون تسجيل الدخول
def apply_coupon(request):
    """
    تطبيق كوبون خصم على سلة التسوق
    """
    serializer = CouponApplySerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'valid': False,
            'message': serializer.errors.get('code', ['كود الكوبون غير صحيح'])[0],
            'discount_amount': 0
        }, status=status.HTTP_400_BAD_REQUEST)

    coupon = serializer.validated_data['code']

    # الحصول على عناصر السلة من الطلب
    cart_items = request.data.get('cart_items', [])
    cart_total = Decimal(str(request.data.get('total', request.data.get('cart_total', 0))))

    # حساب قيمة الخصم
    discount_amount, message = coupon.calculate_discount(cart_items, cart_total)

    if discount_amount <= 0:
        return Response({
            'valid': False,
            'message': message,
            'discount_amount': 0,
            'code': coupon.code
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'valid': True,
        'message': message,
        'discount_amount': float(discount_amount),
        'code': coupon.code,
        'coupon_id': str(coupon.id)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_coupons(request):
    """
    الحصول على قائمة جميع الكوبونات (للمديرين)
    """
    coupons = Coupon.objects.all()
    serializer = CouponSerializer(coupons, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_coupon(request):
    """
    إنشاء كوبون جديد (للمديرين)
    """
    serializer = CouponSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_coupon_detail(request, pk):
    """
    عرض، تحديث أو حذف كوبون محدد (للمديرين)
    """
    try:
        coupon = Coupon.objects.get(pk=pk)
    except Coupon.DoesNotExist:
        return Response({'error': 'الكوبون غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CouponSerializer(coupon)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CouponSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        coupon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def coupon_usage_stats(request, pk):
    """
    الحصول على إحصائيات استخدام كوبون محدد (للمديرين)
    """
    try:
        coupon = Coupon.objects.get(pk=pk)
    except Coupon.DoesNotExist:
        return Response({'error': 'الكوبون غير موجود'}, status=status.HTTP_404_NOT_FOUND)

    usages = CouponUsage.objects.filter(coupon=coupon)
    serializer = CouponUsageSerializer(usages, many=True)

    # حساب إجمالي الخصم
    total_discount = sum(usage.discount_amount for usage in usages)

    return Response({
        'coupon': CouponSerializer(coupon).data,
        'usage_count': usages.count(),
        'total_discount': total_discount,
        'usages': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_coupon_usages(request):
    """
    الحصول على قائمة جميع استخدامات الكوبونات (للمديرين)
    """
    usages = CouponUsage.objects.all()
    serializer = CouponUsageSerializer(usages, many=True)
    return Response(serializer.data)
