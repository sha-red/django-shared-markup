# -*- coding: UTF-8 -*-
# Erik Stein <code@classlibrary.net>, 06/2010

from django.utils.translation import ugettext_lazy as _

from .base import Markup


class HTMLMarkup(Markup):
    def render(self):
        # HTML of course doesn't need to be converted to HTML
        return self.raw or u"" # Make sure that the return value is text
    render.is_safe = True


MARKUP_DESCRIPTION = ('text/html', HTMLMarkup)
