from django.db import models
from django.utils.translation import gettext_lazy as _

class Dashboard(models.Model):
    description = models.CharField(verbose_name=_('description'), max_length=200)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Dashboard')
        verbose_name_plural = _('Dashboard')