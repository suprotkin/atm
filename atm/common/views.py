from django.views import generic


class ErrorPage(generic.TemplateView):
    template_name = 'error_page.html'

    def get_context_data(self, **kwargs):
        context_data = super(ErrorPage, self).get_context_data(**kwargs)
        context_data['custom_error_message'] = self.request.session['_custom_error_message']
        context_data['redirect_to'] = self.request.GET['redirect']
        return context_data
