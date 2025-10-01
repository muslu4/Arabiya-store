from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Avg, Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory
from .serializers import (
    CartSerializer, CartItemSerializer, AddToCartSerializer,
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    OrderStatusUpdateSerializer, OrderStatsSerializer, OrderStatusHistorySerializer
)
from users.utils import send_push_to_user, send_push_to_admins


class CartView(APIView):
    """Get user's cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    """Add item to cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get product
            from products.models import Product
            product = get_object_or_404(Product, id=product_id, is_active=True)
            
            # Check if item already exists in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Update quantity
                new_quantity = cart_item.quantity + quantity
                if new_quantity > product.stock_quantity:
                    return Response({
                        'error': f'الكمية الإجمالية ({new_quantity}) أكبر من المتوفر ({product.stock_quantity})'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                cart_item.quantity = new_quantity
                cart_item.save()
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'تم إضافة المنتج إلى السلة',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartItemView(APIView):
    """Update cart item quantity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response({
                'error': 'عنصر السلة غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Return updated cart
            cart_serializer = CartSerializer(cart_item.cart)
            return Response({
                'message': 'تم تحديث السلة',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFromCartView(APIView):
    """Remove item from cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )
            cart = cart_item.cart
            cart_item.delete()
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'تم حذف المنتج من السلة',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
        except CartItem.DoesNotExist:
            return Response({
                'error': 'عنصر السلة غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):
    """Clear all items from cart"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.clear()
            
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'تم تفريغ السلة',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return Response({
                'message': 'السلة فارغة بالفعل',
                'cart': {'items': [], 'items_count': 0, 'total_amount': 0}
            }, status=status.HTTP_200_OK)


class OrderListView(generics.ListAPIView):
    """List user's orders"""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    """Get order details"""
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    """Create new order"""
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Send notification to user
            try:
                send_push_to_user(
                    order.user.id,
                    "تم إنشاء طلبك",
                    f"تم إنشاء طلب #{order.order_number} بنجاح",
                    {'type': 'order_created', 'order_id': str(order.id)}
                )
            except Exception as e:
                print(f"Failed to send user notification: {e}")
            
            # Send notification to admins
            try:
                send_push_to_admins(
                    "طلب جديد",
                    f"طلب جديد #{order.order_number} من {order.user.get_full_name()}",
                    {'type': 'new_order', 'order_id': str(order.id)}
                )
            except Exception as e:
                print(f"Failed to send admin notification: {e}")
            
            # Return order details
            order_serializer = OrderDetailSerializer(order)
            return Response({
                'message': 'تم إنشاء الطلب بنجاح',
                'order': order_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCancelView(APIView):
    """Cancel order"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({
                'error': 'الطلب غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not order.can_be_cancelled():
            return Response({
                'error': 'لا يمكن إلغاء هذا الطلب'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cancel order
        old_status = order.status
        order.status = 'cancelled'
        order.save()
        
        # Restore stock quantities
        for item in order.items.all():
            item.product.increase_stock(item.quantity)
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status='cancelled',
            notes='تم الإلغاء بواسطة العميل'
        )
        
        # Send notification to admins
        try:
            send_push_to_admins(
                "تم إلغاء طلب",
                f"تم إلغاء الطلب #{order.order_number}",
                {'type': 'order_cancelled', 'order_id': str(order.id)}
            )
        except Exception as e:
            print(f"Failed to send admin notification: {e}")
        
        return Response({
            'message': 'تم إلغاء الطلب بنجاح'
        }, status=status.HTTP_200_OK)


# Admin Views
class AdminOrderListView(generics.ListAPIView):
    """List all orders (Admin only)"""
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بالوصول لهذه البيانات")
        
        queryset = Order.objects.all().order_by('-created_at')
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by payment status
        payment_status = self.request.query_params.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        return queryset


class AdminOrderDetailView(generics.RetrieveAPIView):
    """Get order details (Admin only)"""
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بالوصول لهذه البيانات")
        return Order.objects.all()


class AdminOrderStatusUpdateView(APIView):
    """Update order status (Admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, order_id):
        if not request.user.is_admin:
            raise permissions.PermissionDenied("غير مصرح لك بتحديث حالة الطلبات")
        
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'error': 'الطلب غير موجود'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderStatusUpdateSerializer(
            data=request.data,
            context={'order': order}
        )
        
        if serializer.is_valid():
            old_status = order.status
            new_status = serializer.validated_data['status']
            admin_notes = serializer.validated_data.get('admin_notes', '')
            
            # Update order status
            order.status = new_status
            if admin_notes:
                order.admin_notes = admin_notes
            
            # Update timestamps
            if new_status == 'confirmed' and not order.confirmed_at:
                order.confirmed_at = timezone.now()
            elif new_status == 'shipped' and not order.shipped_at:
                order.shipped_at = timezone.now()
            elif new_status == 'delivered' and not order.delivered_at:
                order.delivered_at = timezone.now()
            
            order.save()
            
            # Create status history
            OrderStatusHistory.objects.create(
                order=order,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user,
                notes=admin_notes or f'تم تحديث الحالة إلى {order.status_display}'
            )
            
            # Send notification to user
            try:
                status_messages = {
                    'confirmed': 'تم تأكيد طلبك',
                    'processing': 'جاري تحضير طلبك',
                    'shipped': 'تم شحن طلبك',
                    'delivered': 'تم تسليم طلبك',
                    'cancelled': 'تم إلغاء طلبك',
                }
                
                message = status_messages.get(new_status, f'تم تحديث حالة طلبك إلى {order.status_display}')
                
                send_push_to_user(
                    order.user.id,
                    "تحديث حالة الطلب",
                    f"{message} #{order.order_number}",
                    {'type': 'order_status_updated', 'order_id': str(order.id), 'status': new_status}
                )
            except Exception as e:
                print(f"Failed to send user notification: {e}")
            
            return Response({
                'message': 'تم تحديث حالة الطلب بنجاح',
                'order': OrderDetailSerializer(order).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_stats(request):
    """Get order statistics (Admin only)"""
    if not request.user.is_admin:
        return Response({
            'error': 'غير مصرح لك بالوصول لهذه البيانات'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Get date range from query params
    days = int(request.query_params.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    orders = Order.objects.filter(created_at__gte=start_date)
    
    stats = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'confirmed_orders': orders.filter(status='confirmed').count(),
        'shipped_orders': orders.filter(status='shipped').count(),
        'delivered_orders': orders.filter(status='delivered').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
        'total_revenue': orders.filter(
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00'),
        'average_order_value': orders.aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0.00'),
    }
    
    serializer = OrderStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_status_history(request, order_id):
    """Get order status history"""
    try:
        order = Order.objects.get(id=order_id)
        
        # Check permissions
        if not request.user.is_admin and order.user != request.user:
            raise permissions.PermissionDenied("غير مصرح لك بالوصول لهذه البيانات")
        
        history = OrderStatusHistory.objects.filter(order=order).order_by('-changed_at')
        serializer = OrderStatusHistorySerializer(history, many=True)
        
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({
            'error': 'الطلب غير موجود'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def shipping_cost_calculator(request):
    """Calculate shipping cost based on city"""
    city = request.query_params.get('city', '').strip()
    
    # Simplified shipping cost calculation
    # In a real application, you would have a more complex system
    shipping_costs = {
        'الرياض': Decimal('15.00'),
        'جدة': Decimal('20.00'),
        'الدمام': Decimal('25.00'),
        'مكة': Decimal('20.00'),
        'المدينة': Decimal('25.00'),
        'الطائف': Decimal('30.00'),
        'تبوك': Decimal('35.00'),
        'أبها': Decimal('35.00'),
        'حائل': Decimal('30.00'),
        'الجوف': Decimal('40.00'),
    }
    
    # Default shipping cost for other cities
    default_cost = Decimal('25.00')
    
    cost = shipping_costs.get(city, default_cost)
    
    return Response({
        'city': city,
        'shipping_cost': cost,
        'currency': 'SAR'
    })