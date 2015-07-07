__author__ = 'roman'

from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models


class CardNumberField(forms.CharField):
    def clean(self, value):
        value = super(CardNumberField, self).clean(value)
        return ''.join(value.split('-'))


class CardNumberForm(forms.Form):
    number = CardNumberField(label=_('number'),
                             widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))

    class Media:
        js = ['js/keyboard_number_input.js', 'js/keyboard.js']


class CardPinForm(forms.Form):
    pin = forms.CharField(label=_('pin'), max_length=4, min_length=4,
                          widget=forms.PasswordInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))

    class Media:
        js = ['js/keyboard_pin_input.js', 'js/keyboard.js']


class CashOutForm(forms.Form):
    amount = forms.DecimalField(
        label=_('amount'), max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control', 'step': '0.1'}))

    class Media:
        js = ['js/keyboard_cash_out.js', 'js/keyboard.js']

