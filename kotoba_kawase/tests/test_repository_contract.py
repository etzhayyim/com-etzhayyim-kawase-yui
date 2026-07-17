from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_canonical_repository_shape() -> None:
    for path in ("manifest.edn", "identity.edn", "dependencies.edn", "repository-contracts.edn"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert text.startswith("{")
    assert not (ROOT / "manifest.jsonld").exists()
    assert len(list((ROOT / "lex").glob("*.edn"))) == 8
    assert len(list((ROOT / "wire").glob("*.json"))) == 8
