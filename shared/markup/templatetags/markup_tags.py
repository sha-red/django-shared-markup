# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2015

import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from .. import markdown_utils


register = template.Library()


@register.filter(needs_autoescape=False)
@stringfilter
def inline_markdown(text, autoescape=None):
    """ Doesn't wrap the markup in a HTML paragraph. """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return markdown_utils.markdown_to_inline_html(esc(text))


@register.filter(needs_autoescape=False)
@stringfilter
def markdown(text, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return markdown_utils.markdown_to_html(esc(text))


@register.filter(needs_autoescape=True)
@stringfilter
def markdown_to_text(text, autoescape=None):
    """
    Converts a string from markdown to HTML, then removes all
    HTML markup (tags and entities).
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return markdown_utils.markdown_to_text(esc(text))


urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')


@register.filter('urlify_markdown')
def urlify_markdown(value):
    value = urlfinder.sub(r'<\1>', value)
    return urlfinder2.sub(r' <\1>', value)
