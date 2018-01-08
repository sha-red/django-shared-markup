# -*- coding: UTF-8 -*-
# Erik Stein <code@classlibrary.net>, 09/2010

import markdown
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _

from .base import Markup
from .pygments import PYGMENTS_INSTALLED


md_filter = markdown.markdown

# try and replace if pygments & codehilite are available
if PYGMENTS_INSTALLED:
    try:
        from markdown.extensions.codehilite import makeExtension
        md_filter = curry(markdown.markdown, extensions=['codehilite(css_class=highlight)'])
    except ImportError:
        pass


class MarkdownMarkup(Markup):
    def render(self):
        return md_filter(self.raw)
    render.is_safe = True


MARKUP_DESCRIPTION = ('text/x-markdown', MarkdownMarkup)
