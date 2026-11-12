from django.contrib import admin
from .models import OrderEnquiry


@admin.register(OrderEnquiry)
class OrderEnquiryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'product', 'quantity_kg', 'preferred_date', 'is_handled', 'created_at')
    list_filter = ('is_handled', 'customer_type', 'product')
    search_fields = ('customer_name', 'phone')