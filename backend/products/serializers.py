from rest_framework import serializers
from .models import Product, Category, Banner

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
    
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

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = '__all__'
        
    def get_image(self, obj):
        # Return the image URL or image_url field
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url or None
        
    def get_link(self, obj):
        # Return the link using the get_link method from the model
        return obj.get_link()

