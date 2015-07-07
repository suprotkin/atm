__author__ = 'roman'
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def logged_card_required(view_func=None):
    def wrapper(request, *args, **kwargs):
        if getattr(request.card, 'number', None) == request.session.get('card_is_logged'):
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('card:number_input'))
    return wrapper

def card_required(view_func=None):
    def wrapper(request, *args, **kwargs):
        if request.card:
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('card:number_input'))
    return wrapper
