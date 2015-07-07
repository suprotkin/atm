from django import http
# from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _

from . import forms
from . import models
from . import _set_card_session_key, logout_card as _logout_card
# Create your views here.


class MainPageView(generic.TemplateView):
    template_name = 'card/operations.html'


class CardNumberInputView(generic.FormView):
    template_name = 'card/number_input.html'
    form_class = forms.CardNumberForm

    def get_success_url(self):
        return reverse('card:pin_input')

    def form_valid(self, form):
        try:
            card = models.Card.objects.get(number=form.cleaned_data['number'])
        except models.Card.DoesNotExist:
            return self.form_invalid(form)
        if card.is_locked:
            return self.form_invalid(form)
        _set_card_session_key(self.request, card)
        return super(CardNumberInputView, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session['_custom_error_message'] = _('Card is locked or invalid card id')
        return http.HttpResponseRedirect('%s?redirect=%s' % (reverse('common:error'), reverse('card:number_input')))


class CardPinView(generic.FormView):
    template_name = 'card/pin_input.html'
    form_class = forms.CardPinForm

    def get_success_url(self):
        return reverse('card:index')

    def form_valid(self, form):
        if self.request.card.pin != form.cleaned_data['pin']:
            self.request.card.try_count += 1
            self.request.card.save()
            return self.form_invalid(form)
        self.request.session['card_is_logged'] = self.request.card.number
        self.request.card.clean_try_count()
        return super(CardPinView, self).form_valid(form)

    def form_invalid(self, form):

        self.request.session['_custom_error_message'] = _('Invalid pin')
        return http.HttpResponseRedirect('%s?redirect=%s' % (reverse('common:error'), reverse('card:pin_input')))


class BalanceView(generic.TemplateView):
    template_name = 'card/balance.html'

    def get(self, request, *args, **kwargs):
        return super(BalanceView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BalanceView, self).get_context_data(**kwargs)
        context.update({
            'card': self.request.card,
            'time': datetime.now(),
            'balance': self.request.card.get_balance()
        })
        return context


class ExitView(generic.RedirectView):
    permanent = False

    def get(self, request, *args, **kwargs):
        _logout_card(request)
        return super(ExitView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('card:index')


class CashOutView(generic.FormView):
    form_class = forms.CashOutForm
    template_name = 'card/cash_out.html'

    def get_success_url(self):
        try:
            last_operation = self.request.card.operations.order_by('-time')[0]
        except IndexError:
            self.request.session['_custom_error_message'] = _('Internal Error. Last operation record is missed')
            return http.HttpResponseRedirect('%s?redirect=%s' % (reverse('common:error'), reverse('card:exit')))
        return reverse('card:cheque', kwargs={'pk': last_operation.pk})

    def form_valid(self, form):
        return \
            self.request.card.get_cash_out(form.cleaned_data['amount']) and super(CashOutView, self).form_valid(form) \
            or self.form_invalid(form)

    def form_invalid(self, form):
        self.request.session['_custom_error_message'] = _('There is no enough money')
        return http.HttpResponseRedirect('%s?redirect=%s' % (reverse('common:error'), reverse('card:exit')))

class ChequeView(generic.DetailView):
    template_name = 'card/balance.html'
    model = models.Operation

    def get_context_data(self, **kwargs):
        context = super(ChequeView, self).get_context_data(**kwargs)
        context.update({
            'card': self.object.card,
            'time': self.object.time,
            'cash_out': self.object.amount,
            'balance': self.object.card._balance
        })
        return context
