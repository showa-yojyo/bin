# -*- coding: utf-8 -*-
"""__init__.py: Language-dependent features.
"""

module_cache = {}

def get_language(lang_code):
    """Return module with language localizations.

    This is a poor copy of the language framework of Docutils.
    """

    if lang_code in module_cache:
        return module_cache[lang_code]

    for i in (1, 0):
        try:
            module = __import__(lang_code, globals(), locals(), level=i)
            break
        except ImportError:
            continue
    else:
        module = __import__('en', globals(), locals(), level=1)

    module_cache[lang_code] = module
    return module
