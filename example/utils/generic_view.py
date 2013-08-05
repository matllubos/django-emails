from django.views.generic.edit import FormView as DjangoFormView
from django.forms.widgets import Media
from django.contrib import messages
from django.utils.encoding import force_unicode

class FormView(DjangoFormView):
    message_valid = ''
    message_invalid = ''
    
    def get_success_url(self):
        if self.success_url:
            return super(FormView, self).get_success_url()
        else:
            return ''
    
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        context['media'] = self.get_media(kwargs.get('form'))
        return context
    
    def get_media(self, form = None):
        media = Media()
        media.add_js(getattr(self.Media, 'js', []))
        media.add_css(getattr(self.Media, 'css', {}))
        if form:
            media += form.media 
        return media
    
    def form_valid(self, form):
        if self.message_valid:
            messages.success(
                self.request,
                force_unicode(self.message_valid),
            )
        form.save()
        return super(FormView, self).form_valid(form)

    def form_invalid(self, form):
        if self.message_invalid:
            messages.error(
                self.request,
                force_unicode(self.message_invalid),
            )
        return super(FormView, self).form_invalid(form)
           
    class Media():
        js = []
        css = {'screen':[], 'print':[]}   