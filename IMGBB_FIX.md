# إصلاح مشكلة ImgBB API

## المشكلة
فشل رفع الصور بسبب عدم تكوين ImgBB API key:
```
ImgBB API key is not configured
```

## الحل
تم تحديث إعدادات ImgBB API في الباكند:

### 1. ملف settings.py
- تم تحديث IMGBB_API_KEY بالقيمة الصحيحة

## الإعدادات المحدثة
```python
IMGBB_API_KEY = config('IMGBB_API_KEY', default='a2cebbc3daff0b042082a5d5d7a3b80d')
```

## الخطوات التالية
1. قم برفع التغييرات إلى المستودع
2. قم بإعادة نشر الباكند على Render

## النتائج المتوقعة
بعد تطبيق هذه التغييرات، يجب أن يعمل رفع الصور بشكل صحيح.
