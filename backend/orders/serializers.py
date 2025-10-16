from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'price', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_phone', 'customer_email', 
            'customer_address', 'governorate', 'additional_info', 
            'payment_method', 'status', 'subtotal', 'delivery_fee', 
            'coupon_code', 'coupon_discount', 'total', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(write_only=True)
    
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_phone', 'customer_email', 
            'customer_address', 'governorate', 'additional_info', 
            'payment_method', 'subtotal', 'delivery_fee', 'coupon_code', 
            'coupon_discount', 'total', 'items'
        ]

    def create(self, validated_data):
        # Extract items from validated data
        items_data = validated_data.pop('items', [])

        # Create the order
        order = Order.objects.create(**validated_data)

        # Create order items and update product stock
        from products.models import Product
        for item_data in items_data:
            product_id = item_data.get('product_id')
            product = Product.objects.get(id=product_id)
            quantity = item_data.get('quantity', 1)
            
            # Create the order item
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item_data.get('product_name', product.name),
                price=item_data.get('price', product.price),
                quantity=quantity,
                total_price=item_data.get('total_price', product.price * quantity)
            )
            
            # Update product stock (decrease by quantity sold)
            if product.stock_quantity >= quantity:
                product.stock_quantity -= quantity
                product.save()

        return order

