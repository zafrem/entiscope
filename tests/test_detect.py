"""Per-text language auto-detection heuristics."""
import pytest

from entiscope._core.detect import detect_language

ALL = ["ko", "en", "ja", "zh"]


def test_hangul_routes_ko():
    assert detect_language("홍길동 010-1234-5678", ALL) == "ko"


def test_latin_routes_en():
    assert detect_language("John Smith 555-123-4567", ALL) == "en"


def test_kana_routes_ja():
    assert detect_language("山田たろう です", ALL) == "ja"


def test_han_without_kana_routes_zh():
    assert detect_language("张伟在北京", ALL) == "zh"


def test_restricted_to_available():
    # Hangul text, but ko not installed → falls back, not ko.
    assert detect_language("홍길동", ["en"]) == "en"  # sole available
    assert detect_language("홍길동", ["en", "ja"]) is None  # ambiguous, ko absent


def test_env_fallback(monkeypatch):
    monkeypatch.setenv("ENTISCOPE_LANG", "en")
    assert detect_language("12345 !!!", ["en", "ja"]) == "en"


def test_no_signal_no_env_returns_none(monkeypatch):
    monkeypatch.delenv("ENTISCOPE_LANG", raising=False)
    assert detect_language("12345 !!!", ["en", "ja"]) is None


def test_distinctive_script_beats_latin():
    # Korean text with an embedded email/URL stays ko: Latin is the weak signal.
    assert detect_language("홍길동 010-1234-5678 a@b.com", ["ko", "en"]) == "ko"
    # Pure Latin (no distinctive script) → en.
    assert detect_language("Meet John at 555-123-4567 tomorrow", ["ko", "en"]) == "en"


@pytest.mark.parametrize("text", ["", "   ", "@@@ ###"])
def test_sole_available_default(text):
    assert detect_language(text, ["ko"]) == "ko"
