from datetime import datetime, timedelta

from smtplib import SMTP

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_unicode

from emails.models import Message, Recipient

class MailSender:
   
    def send_htmlmail(self, sbj, recip, template, context, priority=2, sender=None):
        text = render_to_string(template, context)
        self.send_mails(sbj, recip, text, context, priority, sender)
        
        
    def send_htmlmails(self, sbj, recips, template, context, priority=2, sender=None):
        text = render_to_string(template, context)
        self.send_mails(sbj, recips, text, context, priority, sender)
        
    def send_textmail(self, sbj, recip, text, context, priority=2, sender=None):
        self.send_mails(sbj, recip, text, context, priority, sender)
        
        
    def send_textmails(self, sbj, recips, text, context, priority=2, sender=None):
        self.send_mails(sbj, recips, text, context, priority, sender) 
    
    
    def send_mails(self, sbj, recips, priority, type, context, sender=None):
        if not sender:
            sender = settings.EMAIL_HOST_USER
        
        message = Message.objects.create(
            context = context,
            type = type,
            subject = force_unicode(sbj),
            sender = sender,
            priority = priority
        )  
         
        for recip in recips:   
            Recipient.objects.create(
                mail = recip,
                message = message
            )        
           
    def send(self, sbj, recip, content, sender, mimetype, charset='utf-8'):
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = sbj
        msgRoot['From'] = sender
        msgRoot['To'] =  recip
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
   
        msgAlternative.attach(MIMEText(content, mimetype, _charset=charset))
        
        self.smtp.sendmail(sender, recip, msgRoot.as_string())
    
    def connect(self):
        self.smtp = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        
        if settings.EMAIL_USE_TLS:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo() 
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD :
            self.smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    
    def quit(self):
        self.smtp.quit()
   
    
    def send_batch(self):
        num_send_mails = 0
        messages = Message.objects.filter(datetime__lte = datetime.now(), pk__in = Recipient.objects.filter(sent = False).values('message')).order_by('priority', '-datetime') 
        out = []
        
        if (not messages.exists()):
            out.append("No mass emails to send.")
        else:
            batch = settings.COUNT_MAILS_IN_BATCH
            self.connect()       
            
            i = 0
            while num_send_mails < batch and messages.count() > i:
                message = messages[i]
                recipients = Recipient.objects.filter(message = message, sent = False)

                count_sent_mails = 0   
                for recipient in recipients:
                    self.send(message.subject, recipient.mail, message.content, message.sender, message.type)
                    recipient.sent = True
                    recipient.save()
                    if num_send_mails == batch: break
                    num_send_mails += 1
                    count_sent_mails += 1
                
                out.append(u"Send {0} emails with date {1}.".format(count_sent_mails, message))    
        
                
            self.quit()
            
        self.delete_old_messages()
        return '\n'.join(out)  
    
    def delete_old_messages(self):
        Message.objects.filter(datetime__lte = datetime.now() - timedelta(days=settings.COUNT_DAYS_TO_DELETE_MAIL)).exclude(pk__in = Recipient.objects.filter(sent = False).values('message')).delete()
 
           
        
        
    