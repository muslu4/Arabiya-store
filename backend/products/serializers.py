from rest_framework import serializers
from .models import Product, Category, Banner
from .models_coupons import Coupon, CouponUsage
from .serializers_coupons import CouponSerializer, CouponUsageSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    """A simplified serializer for product lists"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    is_on_sale = serializers.SerializerMethodField()
    stock = serializers.IntegerField(source='stock_quantity', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount_amount', 'discount_percentage', 'discounted_price', 
                  'is_on_sale', 'stock_quantity', 'stock', 'category_name', 'main_image_url', 
                  'image', 'is_featured', 'show_on_homepage', 'brand', 'is_in_stock']

    def get_main_image_url(self, obj):
        if obj.main_image:
            return obj.main_image
        return None

    def get_image(self, obj):
        # Return the first available image
        for img_field in [obj.main_image, obj.image_2, obj.image_3, obj.image_4]:
            if img_field:
                return img_field
        return None
    
    def get_discount_percentage(self, obj):
        """Get discount percentage from model property"""
        return obj.discount_percentage
    
    def get_discounted_price(self, obj):
        """Get discounted price from model property"""
        return obj.discounted_price
    
    def get_is_on_sale(self, obj):
        """Get is_on_sale from model property"""
        return obj.is_on_sale

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    # إضافة حقول الخصم المحسوبة
    discount_percentage = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    is_on_sale = serializers.SerializerMethodField()
    stock = serializers.IntegerField(source='stock_quantity', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name',
            'price', 'discount_amount', 'discount_percentage', 'discounted_price', 'is_on_sale',
            'stock_quantity', 'stock', 'low_stock_threshold',
            'main_image', 'image_2', 'image_3', 'image_4', 'main_image_url', 'image', 'all_images',
            'brand', 'model', 'color', 'size', 'weight',
            'slug', 'meta_description', 'tags',
            'is_active', 'is_featured', 'show_on_homepage', 'display_order',
            'created_at', 'updated_at'
        ]

    def get_main_image_url(self, obj):
        if obj.main_image:
            # main_image is already a URL field, not an ImageField
            return obj.main_image
        return None

    def get_image(self, obj):
        # Return the first available image
        for img_field in [obj.main_image, obj.image_2, obj.image_3, obj.image_4]:
            if img_field:
                return img_field
        return None
    
    def get_all_images(self, obj):
        # Return all product images as a list
        images = []
        for img_field in [obj.main_image, obj.image_2, obj.image_3, obj.image_4]:
            if img_field:
                images.append(img_field)
        return images if images else None
    
    def get_discount_percentage(self, obj):
        """Get discount percentage from model property"""
        return obj.discount_percentage
    
    def get_discounted_price(self, obj):
        """Get discounted price from model property"""
        return obj.discounted_price
    
    def get_is_on_sale(self, obj):
        """Get is_on_sale from model property"""
        return obj.is_on_sale

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_url = serializers.URLField(allow_blank=True, required=False)  # Prefer external URL
    link = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'description', 'image', 'image_url', 'product', 'link_url', 
                  'is_active', 'display_order', 'link', 'product_id', 'created_at', 'updated_at']

    def get_image(self, obj):
        # Prefer external URL (ImgBB) over local file
        image_url = obj.get_image_url()
        print(f"Banner image URL for {obj.title}: {image_url}")
        if image_url and image_url != "#":
            request = self.context.get('request')
            if request and not image_url.startswith('http'):
                # Build absolute URI with proper domain
                absolute_uri = request.build_absolute_uri(image_url)
                print(f"Absolute URI: {absolute_uri}")
                return absolute_uri
            return image_url
        return None

    def get_link(self, obj):
        # Return the link using the get_link method from the model
        link = obj.get_link()
        print(f"Banner link for {obj.title}: {link}")
        return link

    def get_product_id(self, obj):
        # Return the product ID if exists
        if obj.product:
            print(f"Banner {obj.title} is linked to product ID: {obj.product.id}")
            return obj.product.id
        print(f"Banner {obj.title} is not linked to any product")
        return None