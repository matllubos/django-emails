from django import forms
from django.conf import settings


class HtmlWidget(forms.Textarea):
    
    def build_attrs(self, extra_attrs={}, **kwargs):
        extra_attrs['class'] = 'tinymce'
        return super(HtmlWidget, self).build_attrs(extra_attrs, **kwargs)
    
    class Media:
        js = (
              '%sjs/plugins/tinymce/jscripts/tiny_mce/tiny_mce.js' % settings.STATIC_URL,
              '%sjs/plugins/textareas.js' % settings.STATIC_URL,
              )