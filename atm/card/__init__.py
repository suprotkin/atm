from . import models

SESSION_KEY = '_card_id'


def _get_card_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return models.Card._meta.pk.to_python(request.session[SESSION_KEY])


def _set_card_session_key(request, card):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    request.session[SESSION_KEY] = card.pk


def _remove_card_session_key(request):
    request.session[SESSION_KEY] = None
    request.session['card_is_logged'] = None


def logout_card(request):
    _remove_card_session_key(request)
    request._cached_card = None


def get_card(request):
    card = None
    try:
        card_id = _get_card_session_key(request)
    except KeyError:
        pass
    else:
        try:
            card = models.Card.objects.get(id=card_id)
        except models.Card.DoesNotExist:
            pass
    return card
