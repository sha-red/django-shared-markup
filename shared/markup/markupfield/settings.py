# -*- coding: UTF-8 -*-
# Erik Stein <code@classlibrary.net>, 09/2010
"""
Use PREFIX + variable name in your settings file.

Example::

    MARKUP_MARKUP_TYPES
    
"""

import sys
from django.utils.translation import ugettext as _
from django.conf import settings as project_settings


_PREFIX = 'MARKUP_'

defaults = {
    'RST_DEFAULT_LANGUAGE_CODE': getattr(project_settings, 'LANGUAGE_CODE', 'en').split('-')[0],
    'RST_WRITER_NAME': 'html', # 'html4css1'
    'RST_INITIAL_HEADER_LEVEL': 3,
    'RST_DOCTITLE_XFORM': False, # Don't use first section title as document title
    'RST_INPUT_ENCODING': 'utf-8',
    'RST_DEBUG_LEVEL': getattr(project_settings, 'RST_DEBUG_LEVEL', project_settings.DEBUG and 1 or 5),
    'RST_FILTER_SETTINGS': {},
}

__all__ = [defaults]


# Setting up module constants

module = sys.modules[__name__]
for setting_name, default_value in defaults.iteritems():
    setattr(module, setting_name, getattr(project_settings, _PREFIX + setting_name, default_value))
    __all__.append(getattr(module, setting_name))
