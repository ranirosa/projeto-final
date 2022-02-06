from django.core.management.base import BaseCommand, CommandError
from apps.supplies.models import PaymentMethod

class Command(BaseCommand):
    help = 'Creating payment methods'

    def handle(self, *args, **options):
        PaymentMethod.objects.create(description='Cartão de crédito')
        PaymentMethod.objects.create(description='Cartão de débito')
        PaymentMethod.objects.create(description='Multibanco')
        PaymentMethod.objects.create(description='Paypal')
        self.stdout.write(self.style.SUCCESS('Successfully'))

