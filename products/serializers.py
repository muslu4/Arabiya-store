from rest_framework import serializers
from .models import Category, Product, ProductReview, ProductView, Banner


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    products_count = serializers.ReadOnlyField()
    children_count = serializers.ReadOnlyField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'image', 'parent', 'parent_name',
            'is_active', 'products_count', 'children_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'products_count', 'children_count', 'parent_name']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'parent', 'is_active']
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("اسم القسم مطلوب")
        return value.strip()

    def validate(self, attrs):
        parent = attrs.get('parent')
        # Prevent self-parent assignment in update
        if self.instance and parent and self.instance.pk == parent.pk:
            raise serializers.ValidationError("لا يمكن أن يكون القسم أباً لنفسه")
        return attrs


class ProductImageSerializer(serializers.Serializer):
    """Serializer for product images"""
    main_image = serializers.URLField(read_only=True)
    image_2 = serializers.URLField(read_only=True)
    image_3 = serializers.URLField(read_only=True)
    image_4 = serializers.URLField(read_only=True)
    all_images = serializers.ListField(child=serializers.URLField(), read_only=True)


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product list view"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()
    stock_status_display = serializers.ReadOnlyField()
    main_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'price', 
            'discounted_price', 'discount_percentage', 'is_on_sale',
            'stock_quantity', 'is_in_stock', 'stock_status', 'stock_status_display',
            'main_image_url', 'is_featured', 'brand', 'created_at'
        ]
    
    def get_main_image_url(self, obj):
        return obj.main_image or None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product detail view"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()
    stock_status_display = serializers.ReadOnlyField()
    all_images = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'price', 'discounted_price', 'discount_percentage', 'is_on_sale',
            'stock_quantity', 'is_in_stock', 'is_low_stock', 'stock_status', 'stock_status_display',
            'main_image', 'image_2', 'image_3', 'image_4', 'all_images',
            'brand', 'model', 'color', 'size', 'weight',
            'is_featured', 'tags', 'reviews_count', 'average_rating',
            'created_at', 'updated_at'
        ]
    
    def get_all_images(self, obj):
        images = []
        for img in obj.all_images:
            if img:
                images.append(img)
        return images
    
    def get_reviews_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_approved=True)
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            return round(total_rating / reviews.count(), 1)
        return 0


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'category', 'price', 'discount_percentage',
            'stock_quantity', 'low_stock_threshold', 'main_image', 'image_2', 'image_3', 'image_4',
            'brand', 'model', 'color', 'size', 'weight', 'meta_description', 'tags',
            'is_active', 'is_featured'
        ]
    
    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("اسم المنتج مطلوب")
        return value.strip()
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("السعر يجب أن يكون أكبر من صفر")
        return value
    
    def validate_discount_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("نسبة الخصم يجب أن تكون بين 0 و 100")
        return value
    
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("الكمية لا يمكن أن تكون سالبة")
        return value


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'product', 'user', 'user_name', 'rating', 
            'comment', 'is_approved', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'user_name', 'is_approved', 'created_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("التقييم يجب أن يكون بين 1 و 5")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProductSearchSerializer(serializers.ModelSerializer):
    """Serializer for product search results"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    main_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'price', 'discounted_price', 
            'is_on_sale', 'main_image_url', 'brand', 'is_in_stock'
        ]
    
    def get_main_image_url(self, obj):
        return obj.main_image or None


class ProductStatsSerializer(serializers.Serializer):
    """Serializer for product statistics"""
    total_products = serializers.IntegerField()
    active_products = serializers.IntegerField()
    featured_products = serializers.IntegerField()
    out_of_stock_products = serializers.IntegerField()
    low_stock_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_reviews = serializers.IntegerField()


class CategoryStatsSerializer(serializers.Serializer):
    """Serializer for category statistics"""
    category_name = serializers.CharField()
    products_count = serializers.IntegerField()
    active_products_count = serializers.IntegerField()
    total_stock = serializers.IntegerField()


class PopularProductSerializer(serializers.ModelSerializer):
    """Serializer for popular products"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    views_count = serializers.IntegerField()
    main_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category_name', 'price', 'main_image_url', 'views_count'
        ]
    
    def get_main_image_url(self, obj):
        return obj.main_image or None