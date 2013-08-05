from django import forms
from django.utils.translation import ugettext_lazy as _
from emails.engine import MailSender
from utils.widgets import HtmlWidget


class HtmlMailForm(forms.Form):
    recipient_address = forms.EmailField(label=_('Receiver'))
    subject = forms.CharField(label=_('Subject'))
    content = forms.CharField(label=_('Mail content'), widget = HtmlWidget)
    
    def save(self):
        mail_sender = MailSender()
        sbj = self.cleaned_data['subject']
        recip = self.cleaned_data['recipient_address']
        text = self.cleaned_data['content']
        
        mail_sender.send_mail(sbj, recip, text, priority=1, type='html')
    