from django.contrib import admin
from .models import Product
from django.utils.translation import gettext_lazy as _

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'stock', 'stock_limit', 'stock_status', 'price', 'section', 'created_at', 'updated_at')
    list_display_links = ('description',)
    list_filter = ('section',)
    search_fields = ('id', 'description', 'stock', 'price', 'section', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('description', 'price', 'tax', 'discount')
        }),
        (_('Edit stock'), {
            'fields': ('stock', 'stock_limit', 'section')
        })
    )
admin.site.register(Product, ProductAdmin)

