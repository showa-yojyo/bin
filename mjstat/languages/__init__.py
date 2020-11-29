"""__init__.py: Language-dependent features.
"""

from importlib import import_module

module_cache = {}

def get_language(lang_code):
    """Return module with language localizations.

    This is a revamped version of function docutils.languages.get_language.
    """

    if lang_code in module_cache:
        return module_cache[lang_code]

    try:
        module = import_module('.' + lang_code, __name__)
    except ImportError:
        from . import en
        module = en

    module_cache[lang_code] = module
    return module
