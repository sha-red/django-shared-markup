# -*- coding: UTF-8 -*-
# Erik Stein <code@classlibrary.net>, 10/2010

from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget


class MarkupTextarea(forms.widgets.Textarea):
    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, unicode):
            value = value.raw
        return super(MarkupTextarea, self).render(name, value, attrs)


class AdminMarkupTextareaWidget(MarkupTextarea, AdminTextareaWidget):
    pass
