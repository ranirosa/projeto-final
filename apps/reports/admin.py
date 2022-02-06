from unittest import result
from django.contrib import admin
from apps.reports.models import Dashboard
from apps.products.models import Product
from apps.sales.models import ProductSale, Sale
from django.contrib.auth.models import User
from django.urls import path
from django.http import JsonResponse

from apps.supplies.models import ProductOrder, Order
from django.db.models import Count, Sum
import datetime


class DashboardAdmin(admin.ModelAdmin):
    def sales(self):
        sales = ProductSale.objects.all()
        result = 0
        for item in sales:
            result += (item.quantity * item.product.price) - (((item.quantity * item.product.price)*item.discount)/100)
        return result
    
    def orders(self):
        orders = Sale.objects.all().count()
        return orders

    def users(self):
        users = User.objects.all().count()
        return users

    def products(self):
        products = Product.objects.all().count()
        return products
    
    def top_sales(self):
        result = ProductSale.objects.all().values('product__description').annotate(Count('product__description')).order_by('-product__description__count')[:10]
        return result
    
    def last_orders(self):
        result = Sale.objects.all().order_by('-created_at')[:10]
        return result
    
    def top_partners(self):
        result = ProductOrder.objects.all().values('order__partner__name', 'order__partner__id').annotate(Sum('quantity')).order_by('-quantity__sum')[:10]
        return result


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['sales'] = self.sales()
        extra_context['orders'] = self.orders()
        extra_context['users'] = self.users()
        extra_context['products'] = self.products()
        extra_context['table_top_sales'] = self.top_sales()
        extra_context['table_last_sales'] = self.last_orders()
        extra_context['table_top_partners'] = self.top_partners()
        return super(DashboardAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint)),
            path("chart_data_flow/", self.admin_site.admin_view(self.chart_data_flow_endpoint))
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(chart_data, safe=False)
    
    def chart_data_flow_endpoint(self, request):
        chart_data = self.chart_data_flow()
        return JsonResponse(chart_data, safe=False)

    def expense(self):
        expense = ProductOrder.objects.all()
        result = 0
        for item in expense:
            result += item.quantity * item.price
        return result
    
    def profit(self):
        profit = self.sales() - self.expense()
        if profit < 0:
            profit = 0
        return profit

    def chart_data(self):
        return [self.profit(), self.sales(), self.expense()]
    
    def chart_data_flow(self):
        today = datetime.datetime.now()
        sales = []
        expense = []
        profit = []
        labels = []
        for item in range(12):
            result_sales = 0
            result_order = 0
            labels.append(f'{today.strftime("%B")}/{today.year}')
            data_sales = Sale.objects.filter(created_at__year=today.year, created_at__month=today.month)
            for item in data_sales:
                result_sales += item.total
            order = Order.objects.filter(created_at__year=today.year, created_at__month=today.month)
            for item in order:
                result_order += item.total
            today = self.last_month(today, 1)
            sales.append(result_sales)
            expense.append(result_order)
            profit.append(result_sales - result_order)
        labels.reverse()
        sales.reverse()
        expense.reverse()
        profit.reverse()
        # for item in data:
        #     if item.created_at.year >= (today.year - 1):
        #         sales[(int(item.created_at.month) - 1)] += item.total
        # order = Order.objects.all()
        # for item in order:
        #     if item.created_at.year >= (today.year - 1):
        #         expense[(int(item.created_at.month) - 1)] += item.total
        # i = 0
        # for item in profit:
        #     profit[i] = sales[i] - expense[i]
        #     i += 1
        return {
            'labels': labels,
            'data': {
                'profit': profit,
                'sales': sales,
                'expense': expense
            }
        }
    
    def last_month(self, today_date, x):
        new_month = (((today_date.month - 1) - x) % 12) + 1
        new_year  = int(today_date.year + (((today_date.month - 1) - x) / 12 ))
        return datetime.datetime(new_year, new_month, 1)

    
        
admin.site.register(Dashboard, DashboardAdmin)