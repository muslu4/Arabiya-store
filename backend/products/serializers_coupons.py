
from rest_framework import serializers
from .models_coupons import Coupon, CouponUsage


class CouponSerializer(serializers.ModelSerializer):
    """مسلسل بيانات الكوبونات"""
    discount_display = serializers.ReadOnlyField()
    is_valid_display = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = '__all__'

    def get_is_valid_display(self, obj):
        """عرض حالة صلاحية الكوبون"""
        is_valid, message = obj.is_valid()
        return {
            'is_valid': is_valid,
            'message': message
        }

    def validate(self, data):
        """التحقق من صحة البيانات"""
        # التحقق من أن تاريخ الانتهاء بعد تاريخ البدء
        if data.get('end_date') and data.get('start_date'):
            if data['end_date'] <= data['start_date']:
                raise serializers.ValidationError(
                    "تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء"
                )

        # التحقق من قيمة الخصم
        if data.get('discount_type') == 'percentage':
            if data.get('discount_value', 0) > 100:
                raise serializers.ValidationError(
                    "نسبة الخصم لا يمكن أن تتجاوز 100%"
                )

        # التحقق من الحد الأقصى للخصم للكوبونات ذات النسبة المئوية
        if data.get('discount_type') == 'percentage' and not data.get('max_discount_amount'):
            # يمكن إضافة رسالة تحذيرية إذا كان مطلوبًا
            pass

        return data


class CouponUsageSerializer(serializers.ModelSerializer):
    """مسلسل بيانات استخدامات الكوبونات"""
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = CouponUsage
        fields = '__all__'


class CouponApplySerializer(serializers.Serializer):
    """مسلسل بيانات تطبيق الكوبون"""
    code = serializers.CharField(max_length=20)

    def validate_code(self, value):
        """التحقق من صحة كود الكوبون"""
        try:
            coupon = Coupon.objects.get(code=value, is_active=True)
            return coupon
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("كوبون غير صالح أو غير موجود")
