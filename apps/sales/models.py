from django.db import models
from django.contrib.auth.models import User
from apps.supplies.models import PaymentMethod
from apps.products.models import Product
from apps.main.models import Notification
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Client(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE)
    nif = models.CharField(max_length=9)
    address = models.CharField(verbose_name=_('address'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

class SaleStatus(models.Model):
    description = models.CharField(verbose_name=_('description'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Sale status')
        verbose_name_plural = _('Sales status')

class Sale(models.Model):
    client = models.ForeignKey(Client, verbose_name=_('client'), on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, verbose_name=_('payment method'), on_delete=models.CASCADE)
    status = models.ForeignKey(SaleStatus, verbose_name=_('status'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name=_('created at'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    @property
    def total(self):
        data = ProductSale.objects.filter(sale_id= self.id)
        result = 0
        for item in data:
            result += (item.quantity * item.price) - (((item.quantity * item.price) *item.discount) / 100) + (((item.quantity * item.price) *item.tax) / 100)
        if self.status.description == 'Cancelado':
            result = 0
        return result

    def __str__(self):
        return self.client.user.username

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')

class ProductSale(models.Model):
    sale = models.ForeignKey(Sale, verbose_name=_('sale'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_('quantity'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=8, decimal_places=2, editable=False)
    discount = models.IntegerField(verbose_name=_('discount'), editable=False)
    tax = models.IntegerField(verbose_name=_('tax'), editable=False)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Bag')
        verbose_name_plural = _('Bag')
        verbose_name = _('Product sale')
        verbose_name_plural = _('Products sale')

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError(_(f'Quantity must not be greater than the stock. We have just {self.product.stock} in stock.'))

    def save(self, *args, **kwargs):
        my_product = Product.objects.get(id=self.product_id)
        my_product.stock -= self.quantity
        my_product.save()
        self.price = self.product.price
        self.discount = self.product.discount
        self.tax = self.product.tax
        percentage = ((my_product.stock * 100) / my_product.stock_limit)
        if percentage <= 90:
            notification = Notification(
                message = f'Attention! The product {my_product} is {round(percentage)}% out of stock.'
            )
            notification.save()
        super(ProductSale, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.sale.id} - {self.product.description}'