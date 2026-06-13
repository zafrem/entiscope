"""entiscope — multilingual PII detection & masking engine (Apache-2.0).

This is the language-neutral **core**: the two-stage hybrid engine (regex filter
+ ONNX BIOES/Viterbi NER), the ``entiscope`` console command, and the plugin
machinery that discovers installed language packs (``entiscope-ko``,
``entiscope-en``, …). Install at least one language plugin to do real work::

    pip install entiscope-ko            # pulls in this core automatically

Public surface::

    from entiscope import Entiscope
    engine = Entiscope.from_pretrained(lang="ko")   # one language
    auto   = Entiscope.auto()                        # route per text
"""
from ._api import Entiscope
from ._core.schema import RedactionResult, DetectedSpan, SCHEMA_VERSION
from ._core.plugins import LanguagePlugin, installed_languages

__version__ = "0.1.0"

__all__ = [
    "Entiscope",
    "RedactionResult",
    "DetectedSpan",
    "SCHEMA_VERSION",
    "LanguagePlugin",
    "installed_languages",
    "__version__",
]
