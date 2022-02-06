from venv import create
from django.contrib import admin
from .models import (
    Client,
    SaleStatus,
    Sale,
    ProductSale,
)
from apps.main.features import ReverseModelAdmin
from django.urls import path
from django.http import JsonResponse
import datetime
from django.core import serializers
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.urls import resolve

class ClientAdmin(ReverseModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'nif', 'created_at', 'updated_at')
    list_display_links = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'nif')
    inline_type = 'stacked'
    inline_reverse = ['user', ]
admin.site.register(Client, ClientAdmin)

class SaleStatusAdmin(admin.ModelAdmin):
    list_display = ('description', 'created_at', 'updated_at')
    list_display_links = ('description',)
    search_fields = ('description',)
admin.site.register(SaleStatus, SaleStatusAdmin)

class ProductSaleInline(admin.TabularInline):
    model = ProductSale
    extra = 1
    readonly_fields = ('price', 'discount', 'tax')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'payment_method', 'status', 'total', 'created_at', 'updated_at')
    list_display_links = ('client',)
    search_fields = ('client', 'payment_method', 'status', 'created_at', 'updated_at')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SaleAdmin, self).get_fieldsets(request, obj)
        if not request.user.is_superuser and obj != None:
            fieldsets[0][1]['fields'] += ['total']
        return fieldsets

    inlines = [
        ProductSaleInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(SaleAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser and obj is None:
            client = Client.objects.get(user_id=request.user.id)
            form.base_fields['client'].initial = client
            sale_status = SaleStatus.objects.get(id=1)
            form.base_fields['status'].initial = sale_status
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            client = Client.objects.get(user_id=request.user.id)
            if db_field.name == "client":
                kwargs["queryset"] = Client.objects.filter(id=client.id)
            if db_field.name == "status":
                kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super(SaleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        client = Client.objects.filter(user_id=request.user.id)
        return qs.filter(client_id=client[0].id)

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
                data = Sale.objects.all().filter(created_at__year=today.year, created_at__month=today.month).count()
            else:
                client = Client.objects.filter(user_id=request.user.id)
                data = Sale.objects.filter(client_id=client[0].id, created_at__year=today.year, created_at__month=today.month).count()
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
admin.site.register(Sale, SaleAdmin)