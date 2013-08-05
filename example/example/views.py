# Create your views here.
from utils.generic_view import FormView
from .forms import HtmlMailForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class SendMailView(FormView):
    form_class = HtmlMailForm
    message_valid = _('E-mail was sent')
    message_invalid = _('Please correct the following errors')
    template_name = 'send_mail.html'
    
    class Media():
        css = {
               'screen':[
                            '%sadmin/css/base.css' % settings.STATIC_URL,
                            '%scss/screen.css' % settings.STATIC_URL,
                         ]
               } 