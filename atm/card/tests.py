from django.core.urlresolvers import reverse
from django.test import TestCase

from . import models

# Create your tests here.

class Test(TestCase):
    fixtures = ['test_initial.json']
    locked_card = None
    unlocked_card = None
    correct_pin = '1234'
    incorrect_pin = '1111'

    def setUp(self):
        super(Test, self).setUp()
        self.unlocked_card = models.Card.objects.get(id=1)
        self.locked_card = models.Card.objects.get(id=4)

    def check_card(self, card, *args, **kwargs):
        return self.client.post(path=reverse('card:number_input'), data={'number': str(card)}, *args, **kwargs)

    def test_unlocked_cart_number_check(self):
        response = self.check_card(self.unlocked_card, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._request.path, reverse('card:pin_input'))

    def test_locked_card_number_check(self):
        response = self.check_card(self.locked_card, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._request.path, reverse('common:error'))
        self.assertEqual(response._request.GET.get('redirect'), reverse('card:number_input'))

    def test_wrong_pin_card_lock(self):
        self.check_card(self.unlocked_card, follow=True)
        for i in range(4):
            self.assertFalse(self.unlocked_card.is_locked)
            response = self.client.post(reverse('card:pin_input'), data={'pin': self.incorrect_pin}, follow=True)
            self.unlocked_card = models.Card.objects.get(id=self.unlocked_card.id)
            self.assertEqual(response._request.path, reverse('common:error'))
            self.assertEqual(response._request.GET.get('redirect'), reverse('card:pin_input'))
        self.unlocked_card = models.Card.objects.get(id=self.unlocked_card.id)
        self.assertTrue(self.unlocked_card.is_locked)

    def test_card_try_count_clean(self):
        self.check_card(self.unlocked_card, follow=True)
        self.assertEqual(self.unlocked_card.try_count, 0)
        for i in range(3):
            self.client.post(reverse('card:pin_input'), data={'pin': self.incorrect_pin}, follow=True)
            self.unlocked_card = models.Card.objects.get(id=self.unlocked_card.id)
            self.assertEqual(self.unlocked_card.try_count, i+1)
        response = self.client.post(reverse('card:pin_input'), data={'pin': self.correct_pin}, follow=True)
        self.assertEqual(response._request.path, reverse('card:index'))
        self.unlocked_card = models.Card.objects.get(id=self.unlocked_card.id)
        self.assertEqual(self.unlocked_card.try_count, 0)

    def test_exit(self):
        self.check_card(self.unlocked_card, follow=True)
        self.client.post(reverse('card:pin_input'), data={'pin': self.incorrect_pin}, follow=True)
        response = self.client.get(reverse('card:exit'), follow=True)
        self.assertIsNone(response._request.session.get('_card_id'))
        self.assertIsNone(response._request.session.get('card_is_logged'))

    def test_balance_check(self):
        self.check_card(self.unlocked_card, follow=True)
        self.client.post(reverse('card:pin_input'), data={'pin': self.correct_pin}, follow=True)
        response = self.client.get(reverse('card:balance'))
        self.assertEqual(response.status_code, 200)
        last_operation = models.Operation.objects.order_by('-time')[0]
        self.assertEqual(last_operation.card, self.unlocked_card)
        self.assertEqual(last_operation.code, 'balance')

    def _card_withdraw(self, amount):
        self.check_card(self.unlocked_card, follow=True)
        self.client.post(reverse('card:pin_input'), data={'pin': self.correct_pin}, follow=True)
        response = self.client.post(reverse('card:cash_out'), data={'amount': amount}, follow=True)
        self.assertEqual(response.status_code, 200)
        return response

    def test_cash_out(self):
        balance = self.unlocked_card._balance
        response = self._card_withdraw(10)
        self.unlocked_card = models.Card.objects.get(pk=self.unlocked_card.pk)
        self.assertEqual(self.unlocked_card._balance + 10, balance)
        last_operation = models.Operation.objects.order_by('-time')[0]
        self.assertEqual(response._request.path, reverse('card:cheque', kwargs={'pk': last_operation.pk}))
        self.assertEqual(last_operation.card, self.unlocked_card)
        self.assertEqual(last_operation.code, 'cash_out')
        self.assertEqual(last_operation.amount, 10)

    def test_cash_out_overall(self):
        balance = self.unlocked_card._balance
        response = self._card_withdraw(1000)
        self.assertEqual(response._request.path, reverse('common:error'))
        self.unlocked_card = models.Card.objects.get(pk=self.unlocked_card.pk)
        self.assertEqual(self.unlocked_card._balance, balance)
        self.assertEqual(models.Operation.objects.count(), 0)
