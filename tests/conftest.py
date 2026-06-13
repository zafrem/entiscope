import sys
from pathlib import Path

# Allow `import entiscope` when running from a source checkout without install:
# add the project root (which contains the `entiscope` package) to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from entiscope._api import Entiscope  # noqa: E402
from entiscope._core.regex_filter import RegexFilter  # noqa: E402

FIXTURE_RULES = Path(__file__).resolve().parent / "fixtures" / "regex_rules.min.yaml"


@pytest.fixture(scope="session")
def fixture_rules() -> Path:
    return FIXTURE_RULES


@pytest.fixture(scope="module")
def engine() -> Entiscope:
    """A regex-only engine built straight from the fixture ruleset.

    The core ships no language data, so engine tests bypass plugin resolution and
    construct the engine directly from the bundled fixture.
    """
    return Entiscope(RegexFilter.from_yaml(FIXTURE_RULES))
