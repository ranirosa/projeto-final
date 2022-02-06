def notification(request):
    from apps.main.models import Notification
    if request.path_info == '/pf/main/notification/':
        Notification.objects.filter(status=False).update(status=True)
    result = Notification.objects.filter(status=False).count()
    if result > 10:
        result = '+9'
    return {'notification': result}