# -*- coding: UTF-8 -*-
# Erik Stein <code@classlibrary.net>, 09/2010

from django.utils.translation import ugettext_lazy as _
from django.utils.html import linebreaks, urlize


class Markup(object):
    def __init__(self, instance, field_name, rendered_field_name,
                 markup_type_field_name):
        # instead of storing actual values store a reference to the instance
        # along with field names, this makes assignment possible
        self.instance = instance
        self.field_name = field_name
        self.rendered_field_name = rendered_field_name
        self.markup_type_field_name = markup_type_field_name

    # raw is read/write
    def _get_raw(self):
        return self.instance.__dict__[self.field_name]
    def _set_raw(self, value):
        setattr(self.instance, self.field_name, value)
    raw = property(_get_raw, _set_raw)

    # markup_type is read/write
    def _get_markup_type(self):
        return self.instance.__dict__[self.markup_type_field_name]
    def _set_markup_type(self, value):
        return setattr(self.instance, self.markup_type_field_name, value)
    markup_type = property(_get_markup_type, _set_markup_type)

    # rendered is a read only property
    def _get_rendered(self):
        return getattr(self.instance, self.rendered_field_name)
    rendered = property(_get_rendered)

    # allows display via templates to work without safe filter
    def __unicode__(self):
        return self.rendered
    __unicode__.is_safe = True
    
    def render(self, value):
        """
        Must be implemented by subclasses and return the rendered self.raw
        """
        raise NotImplementedError
    render.is_safe = True
    

class PlaintextMarkup(object):
    def render(self, value):
        return urlize(linebreaks(markup))
    render.is_safe = True
    

PLAINTEXT_MARKUP_DESCRIPTION = ('text', PlaintextMarkup)
