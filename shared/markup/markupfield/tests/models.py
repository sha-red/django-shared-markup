from django.db import models

from markupfield.fields import MarkupField
from markupfield.markup import markdown, rst


CUSTOM_MARKUP_TYPES = (
    ('markdown', markdown.MarkdownMarkup),
    rst.MARKUP_DESCRIPTION,
)


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = MarkupField('body of post')

    def __unicode__(self):
        return self.title


class Article(models.Model):
    normal_field = MarkupField()
    markup_choices_field = MarkupField(markup_choices=(('pandamarkup', lambda x: 'panda'),
                                                       ('nomarkup', lambda x: x)))
    default_field = MarkupField(default_markup_type='text/x-markdown')
    markdown_field = MarkupField(markup_type='text/x-markdown')


class Abstract(models.Model):
    content = MarkupField()

    class Meta:
        abstract = True


class Concrete(Abstract):
    pass


class CustomArticle(models.Model):
    text = MarkupField(markup_choices=CUSTOM_MARKUP_TYPES, default_markup_type='text/x-rst')
