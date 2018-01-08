# -*- coding: UTF-8 -*-
# Erik Stein <code@classlibrary.net>, 10/2010

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .markup import DEFAULT_MARKUP_TYPES, Markup
from .widgets import MarkupTextarea, AdminMarkupTextareaWidget


_get_markup_type_field_name = lambda name: '%s_markup_type' % name

def _get_rendered_field_name(name):
    field_name = '%s_rendered' % name
    # Make the field internal
    if not field_name[0] == '_':
        field_name = '_%s' % field_name
    return field_name


class MarkupDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.rendered_field_name = _get_rendered_field_name(self.field.name)
        self.markup_type_field_name = _get_markup_type_field_name(self.field.name)

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("Can only be accessed via an instance.")
        markup = instance.__dict__[self.field.name]
        markup_type = instance.__dict__[self.markup_type_field_name]
        if markup_type is None:
            return None
        if hasattr(self.field.markup_choices_dict[markup_type], 'render'):
            markup_class = self.field.markup_choices_dict[markup_type]
        else:
            # Just a plain filter function, use default Markup class
            if markup is None:
                return None
            markup_class = Markup
        return markup_class(instance, self.field.name, self.rendered_field_name,
                    self.markup_type_field_name)
    
    def __set__(self, obj, value):
        if isinstance(value, Markup):
            obj.__dict__[self.field.name] = value.raw
            setattr(obj, self.rendered_field_name, value.rendered)
            setattr(obj, self.markup_type_field_name, value.markup_type)
        else:
            obj.__dict__[self.field.name] = value
    

class MarkupField(models.TextField):
    def __init__(self, verbose_name=None, name=None, markup_type=None,
                 default_markup_type=None, markup_choices=DEFAULT_MARKUP_TYPES,
                 **kwargs):
        if markup_type and default_markup_type:
            raise ValueError("Cannot specify both markup_type and default_markup_type.")
        # if markup_choices and not default_markup_type:
        #     raise ValueError('No default_markup_type specified.')
        
        self.default_markup_type = markup_type or default_markup_type
        self.markup_type_editable = markup_type is None
        
        # pre 1.0 markup_choices might have been a dict
        if isinstance(markup_choices, dict):
            # raise DeprecationWarning('passing a dictionary as markup_choices is deprecated')
            self.markup_choices_dict = markup_choices
            self.markup_choices_list = markup_choices.keys()
        else:
            self.markup_choices_list = [mc[0] for mc in markup_choices]
            self.markup_choices_dict = dict(markup_choices)
        
        if (self.default_markup_type and
            self.default_markup_type not in self.markup_choices_list):
            raise ValueError("Invalid default_markup_type '%s' for field '%s', allowed values: %s" %
                             (self.default_markup_type, name, ', '.join(self.markup_choices_list)))
        super(MarkupField, self).__init__(verbose_name, name, **kwargs)
    
    def contribute_to_class(self, cls, name):
        if not cls._meta.abstract:
            column_name = self.db_column or name
            choices = zip(self.markup_choices_list, self.markup_choices_list)
            markup_type_field = models.CharField(max_length=30,
                choices=choices, default=self.default_markup_type,
                editable=self.markup_type_editable, blank=self.blank, 
                db_column=_get_markup_type_field_name(column_name))
            rendered_field = models.TextField(editable=False, 
                db_column=_get_rendered_field_name(column_name))
            markup_type_field.creation_counter = self.creation_counter+1
            rendered_field.creation_counter = self.creation_counter+2
            cls.add_to_class(_get_markup_type_field_name(name), markup_type_field)
            cls.add_to_class(_get_rendered_field_name(name), rendered_field)
        super(MarkupField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MarkupDescriptor(self))
    
    def pre_save(self, model_instance, add):
        value = super(MarkupField, self).pre_save(model_instance, add)
        if value.markup_type not in self.markup_choices_list:
            raise ValueError('Invalid markup type (%s), allowed values: %s' %
                             (value.markup_type,
                              ', '.join(self.markup_choices_list)))

        if hasattr(self.markup_choices_dict[value.markup_type], 'render'):
            rendered = value.render()
        else:
            rendered = self.markup_choices_dict[value.markup_type](value.raw)
        setattr(model_instance, _get_rendered_field_name(self.attname), rendered)
        return value.raw
    
    def get_db_prep_value(self, value):
        # for Django 1.2+ rename this to get_prep_value
        if isinstance(value, Markup):
            return value.raw
        else:
            return value
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value.raw
    
    def formfield(self, **kwargs):
        defaults = {'widget': MarkupTextarea}
        defaults.update(kwargs)
        return super(MarkupField, self).formfield(**defaults)


# Register MarkupField to use the custom widget in the Admin
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
FORMFIELD_FOR_DBFIELD_DEFAULTS[MarkupField] = {'widget': AdminMarkupTextareaWidget}
