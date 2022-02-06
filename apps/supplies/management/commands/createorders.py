from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.supplies.models import Order, Partner, PaymentMethod, OrderStatus
from django.contrib.auth.models import User
from random import randint
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Creating random orders'

    def handle(self, *args, **options):
        for i in range(0, 25):
            user = User(username=f'fornecedor_{i}@email.com', first_name=f'fornecedor_{i}')
            user.save()
            x = [str(randint(0, 9)) for p in range(0, 9)]
            var = ''.join(x)
            y = [str(randint(0, 9)) for p in range(0, 9)]
            var1 = ''.join(y)
            partner = Partner(user_id=user.id, name= user.first_name, phone= var, nif= var1, address= f'Rua {i}, número {i}')
            partner.save()
            pm_count = PaymentMethod.objects.all().count()
            pm_rand = randint(1, pm_count)
            pm = PaymentMethod.objects.all()[pm_rand - 1]
            status_count = OrderStatus.objects.all().count()
            status_rand = randint(1, status_count)
            status = OrderStatus.objects.all()[status_rand - 1]
            for j in range(0, 100):
                Order.objects.create(partner_id=partner.id, payment_method_id=pm.id, status_id=status.id, created_at= timezone.now() - timedelta(days=random.randint(0, 365)))
        self.stdout.write(self.style.SUCCESS('Successfully'))