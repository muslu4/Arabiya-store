from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.admin.sites import site
from .models import Category


@staff_member_required
def add_category_view(request):
    """عرض مخصص لإضافة الأقسام"""
    # الحصول على جميع الأقسام لعرضها في القائمة المنسدلة
    categories = Category.objects.all()

    if request.method == 'POST':
        # معالجة النموذج
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active') == 'on'

        # إنشاء القسم الجديد
        category = Category(
            name=name,
            parent_id=parent_id if parent_id else None,
            description=description,
            image=image,
            is_active=is_active
        )
        category.save()

        # إعادة التوجيه إلى صفحة النجاح بعد الإضافة
        return HttpResponseRedirect(reverse('admin:category-add-success', args=[category.id]))

    # عرض النموذج
    return render(request, 'admin/add_category.html', {
        'categories': categories,
        'site': site,
        'has_permission': True,
        'is_popup': False,
        'is_nav_sidebar_enabled': site.enable_nav_sidebar,
        'app_label': 'products',
        'model_name': 'category',
    })


@staff_member_required
def category_list_view(request):
    """عرض مخصص لعرض جميع الأقسام"""
    categories = Category.objects.all()

    return render(request, 'admin/category_list.html', {
        'categories': categories,
        'site': site,
        'has_permission': True,
        'is_popup': False,
        'is_nav_sidebar_enabled': site.enable_nav_sidebar,
        'app_label': 'products',
        'model_name': 'category',
    })


@staff_member_required
def category_add_success_view(request, category_id):
    """عرض صفحة النجاح بعد إضافة قسم"""
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'admin/add_category.html', {
            'error': 'القسم المحدود غير موجود',
            'categories': Category.objects.all(),
            'site': site,
            'has_permission': True,
            'is_popup': False,
            'is_nav_sidebar_enabled': site.enable_nav_sidebar,
            'app_label': 'products',
            'model_name': 'category',
        })
    
    return render(request, 'admin/add_category_success.html', {
        'category': category,
        'site': site,
        'has_permission': True,
        'is_popup': False,
        'is_nav_sidebar_enabled': site.enable_nav_sidebar,
        'app_label': 'products',
        'model_name': 'category',
    })
