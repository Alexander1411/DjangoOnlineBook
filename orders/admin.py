from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['book', 'quantity', 'price']  # Show only these fields in the inline
    readonly_fields = ['book', 'price']  # Make book and price fields read-only if they shouldn't be edited


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'is_paid', 'total_price']
    list_filter = ['is_paid', 'created_at']
    inlines = [OrderItemInline]  # Display OrderItems in the Order admin view
