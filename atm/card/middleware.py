__author__ = 'roman'

from django.utils.functional import SimpleLazyObject

from . import get_card as _get_card


def get_card(request):
    if not hasattr(request, '_cached_card'):
        request._cached_card = _get_card(request)
    return request._cached_card


class CardAuthMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Card authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'card.middleware.CardAuthMiddleware'."
        )
        request.card = SimpleLazyObject(lambda: get_card(request))


