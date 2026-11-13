from .models import OrderEnquiry


def admin_dashboard(request):
    if getattr(request.resolver_match, 'view_name', None) != 'admin:index':
        return {}

    return {
        'dashboard_total': OrderEnquiry.objects.count(),
        'dashboard_open': OrderEnquiry.objects.filter(is_handled=False).count(),
        'dashboard_handled': OrderEnquiry.objects.filter(is_handled=True).count(),
        'dashboard_recent': OrderEnquiry.objects.select_related('customer')[:5],
    }
