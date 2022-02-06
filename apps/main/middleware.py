from apps.sales.models import Client
from apps.supplies.models import Partner

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/pf/login/' in request.META.get('HTTP_REFERER', '') and request.user.id:
            try:
                Client.objects.get(user_id=request.user.id)
                request.path = '/pf/sales/sale/'
                request.path_info = '/pf/sales/sale/'
                response = self.get_response(request)
                return response
            except:
                pass
            try:
                Partner.objects.get(user_id=request.user.id)
                request.path = '/pf/supplies/order/'
                request.path_info = '/pf/supplies/order/'
                response = self.get_response(request)
                return response
            except:
                pass
            request.path = '/pf/reports/dashboard/'
            request.path_info = '/pf/reports/dashboard/'
        response = self.get_response(request)
        return response