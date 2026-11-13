from django.contrib import admin
from django.utils.html import format_html

from .models import OrderEnquiry


@admin.register(OrderEnquiry)
class OrderEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name', 'phone', 'email', 'product', 'quantity_kg',
        'preferred_date', 'status_badge', 'created_at',
    )
    list_filter = ('is_handled', 'customer_type', 'product')
    search_fields = ('customer_name', 'phone', 'email', 'delivery_location')
    date_hierarchy = 'created_at'
    list_per_page = 25

    @admin.display(description='Status', ordering='is_handled')
    def status_badge(self, obj):
        label = 'Reviewed' if obj.is_handled else 'Received'
        status_class = 'is-reviewed' if obj.is_handled else 'is-received'
        return format_html(
            '<span class="enquiry-status {}">{}</span>',
            status_class,
            label,
        )
