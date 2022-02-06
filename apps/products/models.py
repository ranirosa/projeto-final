from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

class Product(models.Model):
    description = models.CharField(verbose_name=_('description'), max_length=200)
    stock = models.IntegerField(verbose_name=_('stock'))
    stock_limit = models.IntegerField(verbose_name=_('stock limit'), default=0)
    price = models.DecimalField(verbose_name=_('price'), max_digits=8, decimal_places=2)
    discount = models.IntegerField(verbose_name=_('discount'))
    tax = models.IntegerField(verbose_name=_('tax'))
    section = models.CharField(verbose_name=_('section'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    @property
    @admin.display(
        description=_('stock status')
    )
    def stock_status(self):
        result = (self.stock * 100) / self.stock_limit
        return f'{round(result)}%'


    def clean(self):
        if self.stock > self.stock_limit:
            raise ValidationError(_('Stock must not be greater than the stock limit.'))

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
