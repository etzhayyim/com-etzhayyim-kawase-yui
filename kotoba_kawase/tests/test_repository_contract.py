import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_canonical_repository_shape() -> None:
    for path in ("manifest.edn", "identity.edn", "dependencies.edn", "repository-contracts.edn"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert text.startswith("{")
    assert not (ROOT / "manifest.jsonld").exists()
    assert len(list((ROOT / "lex").glob("*.edn"))) == 8
    assert len(list((ROOT / "wire").glob("*.json"))) == 8


def test_manifest_and_readme_admit_only_bounded_amm() -> None:
    manifest = (ROOT / "manifest.edn").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    combined = manifest + readme
    assert "constitutionally bounded AMM" in combined
    assert "MAX_PROTOCOL_FEE_BPS" not in combined or "5" in combined
    assert "AMM curve necessarily creates spread" not in combined
    assert "no swap/LP entry points" not in combined
    for independent_quantity in ("LP compensation", "protocol revenue", "price impact"):
        assert independent_quantity in combined


def test_wire_contract_records_bounded_amm_evidence() -> None:
    match = json.loads((ROOT / "wire/matchExecution.json").read_text(encoding="utf-8"))
    props = match["defs"]["main"]["record"]["properties"]
    assert "bounded-amm" in props["settlementMode"]["enum"]
    for field in (
        "ammAdapter", "adapterCodehash", "hookCodehash", "lpFeeBps",
        "protocolFeeBps", "oracleContract", "oracleCodehash",
        "oracleRateBps", "oracleObservedAt", "sequencerUptimeFeed", "executionRateBps",
        "priceImpactBps", "minAmountOutMinor", "deadline",
    ):
        assert field in props
    assert props["lpFeeBps"]["maximum"] == 30
    assert props["protocolFeeBps"]["maximum"] == 5
    assert props["priceImpactBps"]["maximum"] == 50


def test_adr_fixes_the_v4_adapter_security_boundary() -> None:
    adr = (ROOT / "docs/adr/2608011200-constitutional-bounded-amm.md").read_text(
        encoding="utf-8"
    )
    for required_boundary in (
        "exact-input, single-pool adapter",
        "unlock → swap → sync/settle → take",
        "`hookData`",
        "rejects dynamic fees",
        "runtime codehash",
        "global pause",
        "observer must pause execution",
        "callers cannot submit an oracle rate",
        "sequencer uptime feed",
        "pause-only authority",
        "independent security review",
    ):
        assert required_boundary in adr
