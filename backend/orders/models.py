from django.db import models
from django.conf import settings
from products.models import Product
import uuid

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('preparing', 'قيد التحضير'),
        ('shipped', 'قيد الشحن'),
        ('delivered', 'تم التسليم'),
        ('cancelled', 'ملغي'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    customer_phone = models.CharField(max_length=20, verbose_name="رقم هاتف العميل")
    customer_email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    customer_address = models.TextField(verbose_name="عنوان العميل")
    governorate = models.CharField(max_length=50, verbose_name="المحافظة")
    additional_info = models.TextField(blank=True, null=True, verbose_name="ملاحظات إضافية")
    payment_method = models.CharField(max_length=20, choices=[('cash_on_delivery', 'الدفع عند الاستلام'), ('bank_transfer', 'تحويل بنكي')], verbose_name="طريقة الدفع")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المجموع الفرعي")
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5.0, verbose_name="رسوم التوصيل")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المجموع الكلي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    def __str__(self):
        return f"طلب #{self.id} - {self.customer_name}"

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="الطلب")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    name = models.CharField(max_length=100, verbose_name="اسم المنتج")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    quantity = models.IntegerField(verbose_name="الكمية")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الإجمالي")

    def __str__(self):
        return f"{self.quantity} × {self.name}"

    class Meta:
        verbose_name = "عنصر في الطلب"
        verbose_name_plural = "عناصر الطلب"

