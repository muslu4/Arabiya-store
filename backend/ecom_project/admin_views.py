from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from users.models import User
from products.models import Product, Category
from orders.models import Order
from decimal import Decimal

@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard with statistics
    """
    # Get statistics
    users_count = User.objects.count()
    products_count = Product.objects.count()
    orders_count = Order.objects.count()
    categories_count = Category.objects.count()
    
    # Calculate total revenue
    total_revenue = Order.objects.filter(
        status__in=['completed', 'delivered']
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0')
    
    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    
    # Top products
    top_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]
    
    # Monthly statistics (last 6 months)
    from django.utils import timezone
    from datetime import datetime, timedelta
    import calendar
    
    now = timezone.now()
    monthly_stats = []
    
    for i in range(6):
        month_start = now.replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_orders = Order.objects.filter(
            created_at__range=[month_start, month_end]
        ).count()
        
        month_revenue = Order.objects.filter(
            created_at__range=[month_start, month_end],
            status__in=['completed', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
        
        monthly_stats.append({
            'month': calendar.month_name[month_start.month],
            'orders': month_orders,
            'revenue': float(month_revenue)
        })
    
    monthly_stats.reverse()
    
    context = {
        'users_count': users_count,
        'products_count': products_count,
        'orders_count': orders_count,
        'categories_count': categories_count,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'top_products': top_products,
        'monthly_stats': monthly_stats,
    }
    
    return render(request, 'admin/dashboard.html', context)

class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        context['users_count'] = User.objects.count()
        context['products_count'] = Product.objects.count()
        context['orders_count'] = Order.objects.count()
        context['categories_count'] = Category.objects.count()
        
        # Calculate total revenue
        context['total_revenue'] = Order.objects.filter(
            status__in=['completed', 'delivered']
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0')
        
        # Recent activity
        context['recent_orders'] = Order.objects.select_related('user').order_by('-created_at')[:10]
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        context['recent_products'] = Product.objects.order_by('-created_at')[:5]
        
        return context