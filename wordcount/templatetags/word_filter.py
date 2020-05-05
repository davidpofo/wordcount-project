from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def custom_filter(text, wordfreqdict):
    specialwordkeys = wordfreqdict.keys()
    safe_text = ''
    for word in text.split():
        if word in specialwordkeys:
            color = wordfreqdict[word]# returns the hexcode value
            word = '<span style="font-family:Helvetica;font-weight:bold;text-decoration: underline; color:{color}">{word}</span>'.format(color=color, word=word)
        safe_text = safe_text + ' ' + word
    return mark_safe(safe_text)
