# entiscope

**Multilingual PII detection & masking engine** — the language-neutral core of the
[entiscope](https://github.com/zafrem) project.

This package contains the engine (a two-stage hybrid pipeline: a regex filter plus
an optional ONNX BIOES/Viterbi NER stage), the `entiscope` console command, and the
plugin machinery that discovers installed **language packs**. It ships **no language
data** on its own — install at least one language pack to do real work:

```bash
pip install entiscope-ko      # Korean   (pulls in this core automatically)
pip install entiscope-en      # English
```

Installing a language pack pulls in this core as a dependency, so you normally never
`pip install entiscope` directly.

## One command, any combination of languages

The `entiscope` command lives **only** here in the core, so co-installed language
packs never collide over it (each pack only adds its own `entiscope_<lang>` data
package).

```bash
# one language installed → it's used automatically
entiscope redact "홍길동 010-1234-5678"

# several installed → auto-detected per text, or forced with --lang
entiscope redact "John Smith 555-123-4567"          # → English
entiscope redact --lang ko "Call 010-1234-5678"     # force Korean
entiscope --version                                  # lists installed languages
```

## Python API

```python
from entiscope import Entiscope

# one language (explicit, or the sole one installed)
engine = Entiscope.from_pretrained(lang="ko")
engine.redact("홍길동의 전화번호는 010-1234-5678").masked_text   # "<PER>의 전화번호는 <PHONE>"

# multiple languages → route each text automatically
auto = Entiscope.auto()
auto.redact("John Smith 555-123-4567")    # English engine
auto.redact("홍길동 010-1234-5678")        # Korean engine
```

See [`docs/`](../docs) (in the repo) for the CLI reference, offline usage, the
output schema, fine-tuning, and the **multilingual use-case guide**.

## Writing a language pack

A language pack is tiny: a package that ships two YAML files
(`regex_rules.yaml`, `entity_config.yaml`) and registers a `LanguagePlugin` under
the `entiscope.languages` entry-point group.

```python
# entiscope_xx/__init__.py
from entiscope import Entiscope, LanguagePlugin, __version__

LANG = LanguagePlugin(
    code="xx", display_name="Example", default_repo="org/entiscope-xx",
    package="entiscope_xx", scripts=("Latin",), default_base_model="roberta-base",
)
```

```toml
# pyproject.toml
[project]
dependencies = ["entiscope>=0.1.0"]

[project.entry-points."entiscope.languages"]
xx = "entiscope_xx:LANG"
```

## License

Apache-2.0. See [LICENSE](LICENSE).
