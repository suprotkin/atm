from django.db import models
from django.utils.translation import ugettext_lazy as _


OPERATION_CODE_CHOICES = (
    ('balance', _('check card balance')),
    ('cash_out', _('cash out')),
)

class Operation(models.Model):
    card = models.ForeignKey('Card', verbose_name=_('card'), related_name='operations')
    time = models.DateTimeField(_('time'), auto_now_add=True)
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=10, null=True, blank=True)
    code = models.CharField(_('code'), max_length='10', choices=OPERATION_CODE_CHOICES)

    class Meta:
        verbose_name = _('card operation')
        verbose_name_plural = _('card operations')
        ordering = ['card', '-time']

    def __str__(self):
        return '%s: %s' % (self.card, self.code)


class Card(models.Model):
    number = models.CharField(_('number'), max_length=16, unique=True)
    # TODO: pin field should be hashed
    pin = models.CharField(_('pin'), max_length=4)
    is_locked = models.BooleanField(_('is locked'), default=False)
    try_count = models.IntegerField(_('try count'), default=0)
    _balance = models.DecimalField(_('balance'), decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = _('card')
        verbose_name_plural = _('cards')

    def get_balance(self):
        self.operations.create(code="balance")
        return self._balance
    # balance = property(get_balance)

    def __str__(self):
        return u'-'.join([self.number[i:i+4] for i in range(0, 16, 4)])

    def save(self, *args, **kwargs):
        if self.is_locked is False:
            self.is_locked = self.try_count == 4
        super(Card, self).save(*args, **kwargs)

    def clean_try_count(self):
        self.try_count = 0
        self.save()

    def get_cash_out(self, amount):
        if self._balance < amount:
            return False
        self._balance -= amount
        self.operations.create(code='cash_out', amount=amount)
        self.save()
        return True

