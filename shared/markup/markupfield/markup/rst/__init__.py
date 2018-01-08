# -*- coding: utf-8 -*-
# Erik Stein <code@classlibrary.net>, 09/2010

import docutils
import docutils.parsers.rst
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ..base import Markup
from ...settings import (RST_INITIAL_HEADER_LEVEL, RST_WRITER_NAME, 
                         RST_DEFAULT_LANGUAGE_CODE, RST_DOCTITLE_XFORM, 
                         RST_INPUT_ENCODING, RST_DEBUG_LEVEL, RST_FILTER_SETTINGS)
from ..pygments import PYGMENTS_INSTALLED


# Let's you conveniently import the parser
parser = docutils.parsers.rst

try:
    if PYGMENTS_INSTALLED:
        # Register "code" directive for pygments formatting
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, TextLexer
        from pygments.formatters import HtmlFormatter

        DEFAULT = HtmlFormatter()
        VARIANTS = {
            'linenos': HtmlFormatter(linenos=True),
        }

        def pygments_directive(name, arguments, options, content, lineno,
                               content_offset, block_text, state, state_machine):
            try:
                lexer = get_lexer_by_name(arguments[0])
            except ValueError:
                # no lexer found - use the text one instead of an exception
                lexer = TextLexer()
            formatter = options and VARIANTS[options.keys()[0]] or DEFAULT
            parsed = highlight(u'\n'.join(content), lexer, formatter)
            return [docutils.nodes.raw('', parsed, format='html')]
        pygments_directive.arguments = (1, 0, 1)
        pygments_directive.content = 1
        parser.directives.register_directive('code', pygments_directive)
except ImportError:
    pass


class RestructuredtextMarkup(Markup):
    docutils_settings = {
        'language_code': RST_DEFAULT_LANGUAGE_CODE,
        'doctitle_xform': RST_DOCTITLE_XFORM,
        'input_encoding': RST_INPUT_ENCODING,
        'initial_header_level': RST_INITIAL_HEADER_LEVEL,
        'report_level': RST_DEBUG_LEVEL,
    }
    docutils_settings.update(RST_FILTER_SETTINGS)
    
    def render(self, initial_header_level=RST_INITIAL_HEADER_LEVEL, **kwargs):
        """
        Returns the rendered html fragment, i.e. without any html header part.
        """
        settings = self.docutils_settings.copy()
        settings['initial_header_level'] = initial_header_level
        parts = docutils.core.publish_parts(
            source=self.raw, 
            writer_name=WRITER_NAME, 
            settings_overrides=settings
        )
        return parts['fragment']
    render.is_safe = True
    
    def doctree(self, **kwargs):
        """
        Returns the docutils doctree.
        """
        return docutils.core.publish_doctree(self.raw, settings_overrides=self.docutils_settings)

    def title(self, **kwargs):
        """
        Returns the first found title node of a docutils doctree.
        """
        # TODO Why don't we use the 'title' part?
        document = self.doctree()
        matches = document.traverse(condition=lambda node: isinstance(node, docutils.nodes.title))
        if len(matches):
            return matches[0].astext()
        else:
            return None
    
    def plaintext(self, **kwargs):
        return self.doctree().astext()


# Convenience function
def restructuredtext(text, **kwargs):
    rst = RestructuredtextMarkup()
    rst.raw = text
    return rst.render(**kwargs)


MARKUP_DESCRIPTION = ('text/x-rst', RestructuredtextMarkup)
