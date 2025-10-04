from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'name', 'price', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_phone', 'customer_email', 
            'customer_address', 'governorate', 'additional_info', 
            'payment_method', 'status', 'subtotal', 'delivery_fee', 
            'total', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_phone', 'customer_email', 
            'customer_address', 'governorate', 'additional_info', 
            'payment_method', 'subtotal', 'delivery_fee', 'total'
        ]

    def create(self, validated_data):
        # Extract items from the request data
        items_data = self.context.get('items', [])

        # Create the order
        order = Order.objects.create(**validated_data)

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

