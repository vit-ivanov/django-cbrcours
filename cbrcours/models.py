# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrencyLastUpdate(models.Model):
    last_update = models.DateTimeField(_("Last Update"))

    class Meta:
        verbose_name = _('CurrencyLastUpdate')
        verbose_name_plural = _('CurrencyLastUpdates')

    def __unicode__(self):
        return str(self.last_update)

    def save(self, *args, **kwargs):
        '''
        Method is overridden to always had only one object.
        When creating a new object, the old object is overwritten.
        '''
        if self.pk == 1:
            return super(CurrencyLastUpdate, self).save(*args, **kwargs)
        try:
            obj = CurrencyLastUpdate.objects.get(pk=1)
        except CurrencyLastUpdate.DoesNotExist:
            return super(CurrencyLastUpdate, self).save(*args, **kwargs)
        obj.last_update = self.last_update
        obj.save()
        self = obj


class Currency(models.Model):
    code = models.CharField(_('code'), max_length=3)
    name = models.CharField(_('name'), max_length=100)
    value = models.DecimalField(_('value'), max_digits=30, decimal_places=10,
                                help_text=_('Curs Value'))
    nominal = models.PositiveSmallIntegerField(_('Nominal'))

    class Meta:
        ordering = ('name', )
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __unicode__(self):
        return self.code
