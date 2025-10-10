from django.conf import settings

def currency(request):
    """Provide currency symbol and code to all templates"""
    return {
        'CURRENCY_SYMBOL': getattr(settings, 'CURRENCY_SYMBOL', 'د.ع'),
        'CURRENCY_CODE': getattr(settings, 'CURRENCY_CODE', 'IQD'),
    }