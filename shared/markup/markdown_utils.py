# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2012-2016

import markdown as markdown_module
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

import html2text
from shared.utils.text import html_entities_to_unicode


class PseudoParagraphProcessor(markdown_module.blockprocessors.ParagraphProcessor):
    """
    Process paragraph blocks without producing HTML paragraphs.
    """

    def run(self, parent, blocks):
        block = blocks.pop(0)
        if block.strip():
            # Create span element instead of paragraph
            p = markdown_module.util.etree.SubElement(parent, 'span')
            p.text = block.lstrip()


config = dict(
    output_format='html5',
    extensions=[
        'markdown.extensions.extra',  # Includes footnotes
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.admonition',
        'markdown.extensions.smarty',
    ]
)

extensionConfigs = {
    'smarty': {
        'substitutions': {
            'left-single-quote': '&sbquo;',
            'right-single-quote': '&lsquo;',
            'left-double-quote': '&bdquo;',
            'right-double-quote': '&ldquo;'
        }
    }
}


markdown_processor = markdown_module.Markdown(**config)

# Replace ParagraphProcessor
inline_markdown_processor = markdown_module.Markdown(**config)
inline_markdown_processor.parser.blockprocessors['paragraph'] = \
    PseudoParagraphProcessor(inline_markdown_processor.parser)


def markdown_to_inline_html(text, **kwargs):
    kwargs['inline'] = True
    return markdown_to_html(text, **kwargs)

# TODO Decprecated API
inline_markdown = markdown_to_inline_html


def markdown_to_html(text, inline=False, **kwargs):
    if inline:
        processor = inline_markdown_processor
    else:
        processor = markdown_processor
    processor.reset()
    html = processor.convert(text, **kwargs)
    return mark_safe(html)

# TODO Decprecated API
markdown = markdown_to_html


def markdown_to_text(text, **kwargs):
    """
    Converts a string from markdown to HTML, then removes all
    HTML markup (tags and entities).
    """
    html = markdown_to_html(text, **kwargs)
    return strip_tags(html_entities_to_unicode(html))


def html_to_markdown(html):
    return html2text.html2text(html)
