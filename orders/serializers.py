from rest_framework import serializers
from decimal import Decimal
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory
from products.models import Product
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.discounted_price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()
    total_price = serializers.ReadOnlyField()
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_price', 'product_image',
            'quantity', 'total_price', 'is_available', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']
    
    def get_product_image(self, obj):
        if obj.product.main_image:
            return obj.product.main_image.url
        return None
    
    def get_is_available(self, obj):
        return obj.product.is_in_stock and obj.quantity <= obj.product.stock_quantity
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("الكمية يجب أن تكون أكبر من صفر")
        return value
    
    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        
        if product and quantity:
            if not product.is_active:
                raise serializers.ValidationError("هذا المنتج غير متوفر حالياً")
            
            if not product.is_in_stock:
                raise serializers.ValidationError("هذا المنتج نفد من المخزون")
            
            if quantity > product.stock_quantity:
                raise serializers.ValidationError(
                    f"الكمية المطلوبة ({quantity}) أكبر من المتوفر ({product.stock_quantity})"
                )
        
        return attrs


class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart"""
    items = CartItemSerializer(many=True, read_only=True)
    items_count = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'items_count', 'total_amount', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)
    
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
            if not product.is_in_stock:
                raise serializers.ValidationError("هذا المنتج نفد من المخزون")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("المنتج غير موجود")
    
    def validate(self, attrs):
        product_id = attrs['product_id']
        quantity = attrs['quantity']
        
        try:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock_quantity:
                raise serializers.ValidationError(
                    f"الكمية المطلوبة ({quantity}) أكبر من المتوفر ({product.stock_quantity})"
                )
        except Product.DoesNotExist:
            pass  # Already handled in validate_product_id
        
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_price',
            'quantity', 'total_price'
        ]
        read_only_fields = ['id', 'product_name', 'product_price', 'total_price']


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order list view"""
    status_display = serializers.ReadOnlyField()
    payment_status_display = serializers.ReadOnlyField()
    payment_method_display = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'status_display',
            'payment_status', 'payment_status_display',
            'payment_method', 'payment_method_display',
            'total_amount', 'items_count', 'created_at'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for order detail view"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.ReadOnlyField()
    payment_status_display = serializers.ReadOnlyField()
    payment_method_display = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField()
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_name',
            'status', 'status_display', 'payment_status', 'payment_status_display',
            'payment_method', 'payment_method_display',
            'subtotal', 'discount_amount', 'shipping_cost', 'tax_amount', 'total_amount',
            'shipping_name', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_postal_code',
            'notes', 'admin_notes', 'items', 'items_count',
            'created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'
        ]


class CustomerDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True)
    address = serializers.CharField(max_length=255)
    governorate = serializers.CharField(max_length=100)

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    customer = CustomerDataSerializer(write_only=True)
    additional_info = serializers.CharField(required=False, allow_blank=True, source='notes')

    class Meta:
        model = Order
        fields = [
            'customer',
            'payment_method',
            'additional_info'
        ]

    def validate(self, data):
        customer_data = data.get('customer')
        if not customer_data.get('name', '').strip():
            raise serializers.ValidationError({"customer": {"name": "اسم المستلم مطلوب"}})
        if not customer_data.get('phone', '').strip():
            raise serializers.ValidationError({"customer": {"phone": "هاتف المستلم مطلوب"}})
        if not customer_data.get('address', '').strip():
            raise serializers.ValidationError({"customer": {"address": "عنوان الشحن مطلوب"}})
        if not customer_data.get('governorate', '').strip():
            raise serializers.ValidationError({"customer": {"governorate": "المدينة مطلوبة"}})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        customer_data = validated_data.pop('customer')

        # Get user's cart
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("السلة فارغة")

        if not cart.items.exists():
            raise serializers.ValidationError("السلة فارغة")

        # Calculate order totals
        subtotal = Decimal('0.00')
        for cart_item in cart.items.all():
            if not cart_item.product.is_active or not cart_item.product.is_in_stock:
                raise serializers.ValidationError(
                    f"المنتج '{cart_item.product.name}' غير متوفر حالياً"
                )
            
            if cart_item.quantity > cart_item.product.stock_quantity:
                raise serializers.ValidationError(
                    f"الكمية المطلوبة من '{cart_item.product.name}' ({cart_item.quantity}) "
                    f"أكبر من المتوفر ({cart_item.product.stock_quantity})"
                )
            
            subtotal += cart_item.total_price
        
        # Calculate shipping cost (simplified - you can implement complex logic)
        shipping_cost = Decimal('5.00')  # Fixed shipping cost
        
        # Calculate tax (example, can be adjusted)
        tax_amount = Decimal('0.00')
        
        # Create order
        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            shipping_name=customer_data['name'],
            shipping_phone=customer_data['phone'],
            shipping_address=customer_data['address'],
            shipping_city=customer_data['governorate'],
            **validated_data
        )
        
        # Create order items and reduce stock
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            
            # Reduce product stock
            cart_item.product.reduce_stock(cart_item.quantity)
        
        # Clear cart
        cart.clear()
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            new_status='pending',
            notes='تم إنشاء الطلب'
        )
        
        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    admin_notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_status(self, value):
        order = self.context.get('order')
        if not order:
            return value
        
        # Define valid status transitions
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['processing', 'cancelled'],
            'processing': ['shipped', 'cancelled'],
            'shipped': ['delivered'],
            'delivered': ['returned'],
            'cancelled': [],
            'returned': []
        }
        
        if value not in valid_transitions.get(order.status, []):
            raise serializers.ValidationError(
                f"لا يمكن تغيير حالة الطلب من '{order.status_display}' إلى '{dict(Order.STATUS_CHOICES)[value]}'"
            )
        
        return value


class OrderStatsSerializer(serializers.Serializer):
    """Serializer for order statistics"""
    total_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    confirmed_orders = serializers.IntegerField()
    shipped_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for order status history"""
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)
    old_status_display = serializers.SerializerMethodField()
    new_status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderStatusHistory
        fields = [
            'id', 'old_status', 'old_status_display',
            'new_status', 'new_status_display',
            'changed_by', 'changed_by_name', 'notes', 'changed_at'
        ]
    
    def get_old_status_display(self, obj):
        if obj.old_status:
            return dict(Order.STATUS_CHOICES).get(obj.old_status, obj.old_status)
        return ''
    
    def get_new_status_display(self, obj):
        return dict(Order.STATUS_CHOICES).get(obj.new_status, obj.new_status)