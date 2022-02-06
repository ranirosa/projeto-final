from django.core.management.base import BaseCommand
from apps.products.models import Product
from apps.sales.models import Sale, Client, PaymentMethod, SaleStatus, ProductSale
from apps.supplies.models import Partner, Order, PartnerProduct, OrderStatus, ProductOrder
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Creating random sales'

    def handle(self, *args, **options):
        for i in range(51, 100):
            user = User(username=f'utilizador_{i}@email.com', first_name=f'utilizador_{i}')
            user.save()
            x = [str(randint(0, 9)) for p in range(0, 9)]
            var = ''.join(x)
            client = Client(user_id=user.id, nif= var, address= f'Rua {i}, número {i}')
            client.save()
            pm_count = PaymentMethod.objects.all().count()
            pm_rand = randint(1, pm_count)
            pm = PaymentMethod.objects.all()[pm_rand - 1]
            status_count = SaleStatus.objects.all().count()
            status_rand = randint(1, status_count)
            status = SaleStatus.objects.all()[status_rand - 1]
            for j in range(0, 5):
                sales = Sale(client_id=client.id, payment_method_id=pm.id, status_id=status.id, created_at= timezone.now() - timedelta(days=random.randint(0, 365)))
                sales.save()
                n_products = randint(1, 5)
                n = 1
                while n <= n_products:
                    p_count = Product.objects.all().count()
                    p_rand = randint(1, p_count)
                    p = Product.objects.all()[p_rand - 1]
                    if ((p.stock * 100) / p.stock_limit) < 90:
                        partner_product = PartnerProduct.objects.filter(product_id= p.id).order_by('price')
                        status_count = OrderStatus.objects.all().count()
                        status_rand = randint(1, status_count)
                        order_status = OrderStatus.objects.all()[status_rand - 1]
                        if partner_product.exists():
                            order = Order(partner_id= partner_product[0].partner.id, payment_method_id=pm.id, status_id=order_status.id, created_at= timezone.now() - timedelta(days=random.randint(0, 365)))
                            order.save()
                            ProductOrder.objects.create(product_id=partner_product[0].id, order_id=order.id, quantity=(p.stock_limit - p.stock))
                        else:
                            user_partner = User(username=f'parceiro_{i}{j}{n}@email.com', first_name=f'parceiro_{i}{j}{n}')
                            user_partner.save()
                            x = [str(randint(0, 9)) for p in range(0, 9)]
                            var = ''.join(x)
                            y = [str(randint(0, 9)) for p in range(0, 9)]
                            var1 = ''.join(y)
                            partner = Partner(user_id=user_partner.id, name= f'parceiro_{i}{j}{n} Companhia Lda', phone= var, nif= var1, address= f'Rua {i}, número {i}')
                            partner.save()
                            partner_product = PartnerProduct(product_id=p.id, partner_id=partner.id, price=((p.price * 70) / 100), discount=0, tax= 0)
                            partner_product.save()
                            order = Order(partner_id= partner_product.partner.id, payment_method_id=pm.id, status_id=order_status.id, created_at= timezone.now() - timedelta(days=random.randint(0, 365)))
                            order.save()
                            ProductOrder.objects.create(product_id=partner_product.id, order_id=order.id, quantity=(p.stock_limit - p.stock))
                    ProductSale.objects.create(sale_id= sales.id, product_id= p.id, quantity= randint(1, 5))
                    n += 1
        self.stdout.write(self.style.SUCCESS('Successfully'))