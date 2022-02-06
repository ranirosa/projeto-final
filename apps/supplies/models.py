from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.products.models import Product
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    description = models.CharField(verbose_name=_('description'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    

class Partner(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    phone = models.CharField(verbose_name=_('phone'), max_length=13)
    address = models.CharField(verbose_name=_('address'), max_length=200)
    nif = models.CharField(max_length=9)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')
    

class Contact(models.Model):
    partner = models.ForeignKey(Partner, verbose_name=_('partner'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    sector = models.CharField(verbose_name=_('sector'), max_length=200)
    category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.CASCADE)
    value = models.CharField(verbose_name=_('value'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
    

class PartnerProduct(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, verbose_name=_('partner'), on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name=_('price'), max_digits=8, decimal_places=2)
    discount = models.IntegerField(verbose_name=_('discount'))
    tax = models.IntegerField(verbose_name=_('tax'))
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    class Meta:
        unique_together = ('product', 'partner')
        verbose_name = _('Partner product')
        verbose_name_plural = _('Partner products')

    def __str__(self):
        return f'{self.product.description} - {self.partner.name}'

class PaymentMethod(models.Model):
    description = models.CharField(verbose_name=_('description'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Payment method')
        verbose_name_plural = _('Payment methods')

class OrderStatus(models.Model):
    description = models.CharField(verbose_name=_('description'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Order status')
        verbose_name_plural = _('Orders status')


class Order(models.Model):
    partner = models.ForeignKey(Partner, verbose_name=_('partner'), on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, verbose_name=_('payment method'), on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, verbose_name=_('status'), on_delete=models.CASCADE)
    invoice = models.CharField(verbose_name=_('invoice'), null=True, blank=True, max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    @property
    def total(self):
        data = ProductOrder.objects.filter(order_id= self.id)
        result = 0
        for item in data:
            result += (item.quantity * item.price) - (((item.quantity * item.price) *item.discount) / 100) + (((item.quantity * item.price) *item.tax) / 100)
        return result

    def __str__(self):
        return f'{self.invoice if self.invoice else ""} {"-" if self.invoice else ""} {self.partner} - {self.status}'

    def clean(self):
        product_order = ProductOrder.objects.filter(order_id=self.id).exclude(product__partner__id=self.partner_id)
        if product_order.exists():
            raise ValidationError(_("We can't request a product in an other partner."))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('order'), on_delete=models.CASCADE)
    product = models.ForeignKey(PartnerProduct,verbose_name=_('product'), on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_('quantity'))
    price = models.DecimalField(verbose_name=_('price'), max_digits=8, decimal_places=2, editable=False)
    discount = models.IntegerField(verbose_name=_('discount'), editable=False)
    tax = models.IntegerField(verbose_name=_('tax'), editable=False)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def clean(self):
        if self.quantity > (self.product.product.stock_limit - self.product.product.stock):
            raise ValidationError(_('Quantity must not be greater than the stock limit.'))
    
    def save(self, *args, **kwargs):
        my_product = Product.objects.get(id=self.product.product_id)
        my_product.stock += self.quantity
        my_product.save()
        self.price = self.product.price
        self.discount = self.product.discount
        self.tax = self.product.tax
        super(ProductOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order} - {self.product}'

    class Meta:
        verbose_name = _('Product order')
        verbose_name_plural = _('Products order')






    
