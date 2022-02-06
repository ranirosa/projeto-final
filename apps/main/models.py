from django.db import models
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    message = models.CharField(verbose_name=_('message'), max_length=200)
    status = models.BooleanField(verbose_name=_('status'), default=False)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')