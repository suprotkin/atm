__author__ = 'roman'

from django.conf.urls import url
from .decorators import card_required, logged_card_required
from . import views

urlpatterns = [
    url(r'number/$', views.CardNumberInputView.as_view(), name='number_input'),
    url(r'pin/$', card_required(views.CardPinView.as_view()), name='pin_input'),
    url(r'balance/$', card_required(logged_card_required(views.BalanceView.as_view())), name='balance'),
    url(r'cash_out/$', card_required(logged_card_required(views.CashOutView.as_view())), name='cash_out'),
    url(r'cheque/(?P<pk>\d+)/$', card_required(logged_card_required(views.ChequeView.as_view())), name='cheque'),
    url(r'exit/$', views.ExitView.as_view(), name='exit'),
    url(r'$', card_required(logged_card_required(views.MainPageView.as_view())), name='index'),
]
