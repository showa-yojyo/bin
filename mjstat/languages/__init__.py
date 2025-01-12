"""__init__.py: Language-dependent features."""

from importlib import import_module
from types import ModuleType

module_cache: dict[str, ModuleType] = {}


def get_language(lang_code: str) -> ModuleType:
    """Return module with language localizations.

    This is a revamped version of function docutils.languages.get_language.
    """

    global module_cache
    if lang_code in module_cache:
        return module_cache[lang_code]

    try:
        module = import_module("." + lang_code, __name__)
    except ImportError:
        from . import en

        module = en

    module_cache[lang_code] = module
    return module
