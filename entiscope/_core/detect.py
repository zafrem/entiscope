"""Per-text language auto-detection via Unicode-script heuristics.

Pure stdlib, no new dependencies. Detection is **restricted to the set of
installed/available language codes**, so the router never picks a language the
user has not installed. Used by :meth:`entiscope.Entiscope.auto` and the CLI when
multiple language plugins are present and no ``--lang`` was given.
"""
from __future__ import annotations

import os
import unicodedata
from typing import Dict, Iterable, List, Optional, Tuple


def _script_counts(text: str) -> Dict[str, int]:
    counts = {"Hangul": 0, "Hiragana": 0, "Katakana": 0, "Han": 0, "Latin": 0}
    for ch in text:
        if not ch.isalpha():
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:  # unnamed char
            continue
        if "HANGUL" in name:
            counts["Hangul"] += 1
        elif "HIRAGANA" in name:
            counts["Hiragana"] += 1
        elif "KATAKANA" in name:
            counts["Katakana"] += 1
        elif "CJK" in name:
            counts["Han"] += 1
        elif "LATIN" in name:
            counts["Latin"] += 1
    return counts


def detect_language(text: str, available: Iterable[str]) -> Optional[str]:
    """Return the best language code in ``available`` for ``text``, or ``None``.

    Heuristic: Hangul → ko, kana → ja, Han-without-kana → zh, otherwise Latin →
    en. Distinctive scripts (Hangul/kana/Han) outrank Latin — Latin appears in
    every language's text (emails, URLs), so any Hangul beats an embedded
    ``a@b.com``. Falls back to ``$ENTISCOPE_LANG``, then the sole available
    language, else ``None``.
    """
    avail = set(available)
    c = _script_counts(text)
    has_kana = bool(c["Hiragana"] or c["Katakana"])

    # Distinctive scripts are strong language signals and outrank Latin.
    distinctive: List[Tuple[str, int]] = []
    if c["Hangul"]:
        distinctive.append(("ko", c["Hangul"]))
    if has_kana:
        distinctive.append(("ja", c["Hiragana"] + c["Katakana"]))
    if c["Han"]:
        # Han mixed with kana is Japanese; Han alone leans Chinese.
        distinctive.append(("ja" if has_kana else "zh", c["Han"]))

    for code, _score in sorted(distinctive, key=lambda kv: kv[1], reverse=True):
        if code in avail:
            return code
    if c["Latin"] and "en" in avail:
        return "en"

    env = os.environ.get("ENTISCOPE_LANG")
    if env and env in avail:
        return env
    if len(avail) == 1:
        return next(iter(avail))
    return None
