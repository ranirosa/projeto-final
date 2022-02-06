from django.contrib import admin
from .models import Notification
from django.views.decorators.cache import never_cache

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'updated_at')
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_import_permission(self, request, obj=None):
        return False
        
    @never_cache
    def index(self, request, extra_context=None):
        Notification.objects.filter(status=False).update(status=True)
        super(NotificationAdmin, self).index(request, extra_context)

admin.site.register(Notification, NotificationAdmin)
