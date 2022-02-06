from django.contrib import admin
from .models import (
    Category, 
    Contact, 
    Partner, 
    PartnerProduct, 
    PaymentMethod, 
    OrderStatus,
    Order,
    ProductOrder
)
from django.urls import path
from django.http import JsonResponse
import datetime
from apps.main.features import ReverseModelAdmin

from django.urls import resolve


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_at', 'updated_at')
    list_display_links = ('description',)
    search_fields = ('description',)
admin.site.register(Category, CategoryAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'category', 'value', 'created_at', 'updated_at')
    list_display_links = ('name',)
    search_fields = ('name', 'sector', 'category', 'value', 'created_at', 'updated_at')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            partner = Partner.objects.get(user_id=request.user.id)
            if db_field.name == "partner":
                kwargs["queryset"] = Partner.objects.filter(id=partner.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(ContactAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        partner = Partner.objects.filter(user_id=request.user.id)
        return qs.filter(partner_id=partner[0].id)
admin.site.register(Contact, ContactAdmin)

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address',  'nif', 'created_at', 'updated_at')
    list_display_links = ('name',)
    search_fields = ('name', 'phone', 'address',  'nif', 'created_at', 'updated_at')
    inlines = [
        ContactInline,
    ]
    inline_type = 'stacked'
    inline_reverse = ['user', ]

    def get_queryset(self, request):
        qs = super(PartnerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        partner = Partner.objects.filter(user_id=request.user.id)
        return qs.filter(id=partner[0].id)
admin.site.register(Partner, PartnerAdmin)

class PartnerProductAdmin(admin.ModelAdmin):
    list_display = ('partner', 'product', 'price', 'discount', 'tax', 'created_at', 'updated_at')
    list_display_links = ('partner',)
    list_filter = ('partner',)
    search_fields = ('partner', 'product', 'price', 'discount', 'tax', 'created_at', 'updated_at')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PartnerProductAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser and obj is None:
            partner = Partner.objects.get(user_id=request.user.id)
            form.base_fields['partner'].initial = partner
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            partner = Partner.objects.get(user_id=request.user.id)
            if db_field.name == "partner":
                kwargs["queryset"] = Partner.objects.filter(id=partner.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    def get_queryset(self, request):
        qs = super(PartnerProductAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        partner = Partner.objects.filter(user_id=request.user.id)
        return qs.filter(partner_id=partner[0].id)
admin.site.register(PartnerProduct, PartnerProductAdmin)

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_at', 'updated_at')
    list_display_links = ('description',)
    search_fields = ('description', 'created_at', 'updated_at')
admin.site.register(PaymentMethod, PaymentMethodAdmin)

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_at', 'updated_at')
    list_display_links = ('description',)
    search_fields = ('description', 'created_at', 'updated_at')
admin.site.register(OrderStatus, OrderStatusAdmin) 

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if request.method == 'POST':
            return ()
        if obj is not None:
            return ('price', 'discount', 'tax')
        else:
            return ()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        resolved = resolve(request.path_info)
        order = Order.objects.get(id=resolved.kwargs['object_id'])
        if db_field.name == "product":
            kwargs["queryset"] = PartnerProduct.objects.filter(partner__id=order.partner_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('partner', 'payment_method', 'total', 'status', 'invoice', 'created_at', 'updated_at')
    list_display_links = ('partner',)
    search_fields = ('partner', 'payment_method', 'status', 'invoice', 'created_at', 'updated_at')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(OrderAdmin, self).get_fieldsets(request, obj)
        if not request.user.is_superuser and not obj is None:
            fieldsets[0][1]['fields'] += ['total']
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser and obj is None:
            partner = Partner.objects.get(user_id=request.user.id)
            form.base_fields['partner'].initial = partner
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            partner = Partner.objects.get(user_id=request.user.id)
            if db_field.name == "partner":
                kwargs["queryset"] = Partner.objects.filter(id=partner.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        partner = Partner.objects.filter(user_id=request.user.id)
        return qs.filter(partner_id=partner[0].id)
        
    def get_inlines(self, request, obj):
        if obj and obj.partner_id:
            return [ProductOrderInline]
        return []

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data(request)
        return JsonResponse(chart_data, safe=False)

    def chart_data(self, request):
        today = datetime.datetime.now()
        
        result = []
        labels = []
        for item in range(12):
            labels.append(f'{today.strftime("%B")}/{today.year}')
            if request.user.is_superuser:
                data = Order.objects.all().filter(created_at__year=today.year, created_at__month=today.month).count()
            else:
                partner = Partner.objects.filter(user_id=request.user.id)
                data = Order.objects.filter(partner_id=partner[0].id, created_at__year=today.year, created_at__month=today.month).count()
            result.append(data)
            today = self.last_month(today, 1)
        labels.reverse()
        result.reverse()
        return {
            'labels': labels,
            'data': result
        }

    def last_month(self, today_date, x):
        new_month = (((today_date.month - 1) - x) % 12) + 1
        new_year  = int(today_date.year + (((today_date.month - 1) - x) / 12 ))
        return datetime.datetime(new_year, new_month, 1)
admin.site.register(Order, OrderAdmin)

