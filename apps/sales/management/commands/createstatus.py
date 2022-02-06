from django.core.management.base import BaseCommand
from apps.sales.models import SaleStatus

class Command(BaseCommand):
    help = 'Creating status'

    def handle(self, *args, **options):
        SaleStatus.objects.create(description='Aceito')
        SaleStatus.objects.create(description='Em progresso')
        SaleStatus.objects.create(description='Em trânsito')
        SaleStatus.objects.create(description='Em entrega')
        SaleStatus.objects.create(description='Entregue')
        self.stdout.write(self.style.SUCCESS('Successfully'))