from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    link = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'description', 'image', 'product', 'product_name',
            'link_url', 'link', 'is_active', 'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_link(self, obj):
        return obj.get_link()

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("عنوان الإعلان مطلوب")
        return value.strip()

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("صورة الإعلان مطلوبة")
        return value