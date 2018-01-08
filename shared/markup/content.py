# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, linebreaks

from .utils import markdown_to_html


class MarkupContent(models.Model):
    PLAIN_TEXT = 'text/plain'
    MARKDOWN = 'text/x-markdown'
    HTML = 'text/html'
    MARKUP_FORMATS = (
        (MARKDOWN, _("Markdown")),
        (PLAIN_TEXT, _("Reiner Text")),
        (HTML, _("HTML")),
    )
    markup_format = models.CharField(max_length=20, choices=MARKUP_FORMATS, default=MARKDOWN)
    content = models.TextField(_("text"))
    css_class = models.CharField(_("CSS-Klasse"), max_length=50, help_text=_("Über die CSS-Klasse kann die Darstellung gesteuert werden."), null=True, blank=True)

    class Meta:
        abstract = True

    def render(self, inline=False, **kwargs):
        if self.markup_format == self.MARKDOWN:
            # Marked safe by the markdown converter
            return markdown_to_html(self.content, inline=inline)

        elif self.markup_format == self.HTML:
            return mark_safe(self.content)

        else:
            return linebreaks(conditional_escape(self.content))
