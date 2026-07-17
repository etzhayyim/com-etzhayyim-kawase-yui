# com.etzhayyim.kawase.* — kawase-yui (為替結) Lexicons

**Owner actor**: `did:web:kawase-yui.etzhayyim.com` (`com-etzhayyim-kawase-yui`)
**ADR**: ADR-2605282200 (R0 scaffold; landed 2026-05-28)
**Status**: R0 schemas — full structural enforcement at the const-field
layer. R1 wiring lands post-Bootstrap-Council Seats 2-5 close
(RFP 2026-06-19).

## 8 Lexicons

| # | Lexicon | Producer cell | Consumer | Purpose |
|---|---|---|---|---|
| L1 | `depositAttestation` | kotoba_kawase.send → KawaseYuiPool.deposit | `kawase_pool_match` cell | Sender-side L1 Quad — CACAO-signed by sender DID; locked fxRateBps + fxRateAttestationCid + perMonthCapRemainingMinor + optional encryptedMemoCid (ADR-2605181100) |
| L2 | `withdrawIntent` | kotoba_kawase (recipient pre-declare) | `kawase_pool_match` cell | Recipient-side L1 Quad expressing match interest; advisory (not binding); validUntil default = createdAt + 30 days |
| L3 | `matchExecution` | `kawase_pool_match` cell | `kawase_silen_review` + toritate.annualReport | Match engine output; settlementMode ∈ {matched, reserve-disbursed}; mKotoDebitAmount per cell tick; executingCellDid MUST be fleet.toml-listed (G12) |
| L4 | `fxRateAttestation` | `kawase_fx_oracle_watcher` cell | `kawase_pool_match` + `depositAttestation` | Chainlink mid-market snapshot; councilBandBps reads Constitution.KAWASE_MAX_BAND_BPS=50; withinBand=false halts ALL pair matching until Council Lv6+ ≥3 resumes |
| L5 | `poolStateReport` | `kawase_pool_match` cell | toritate.annualReport | Per-currency aggregate (no per-member amounts); driftBps>500 triggers rebalanceAttestation candidate; mKotoConsumedThisEpoch rollup |
| L6 | `rebalanceAttestation` | `kawase_rebalance_proposer` cell → KawaseYuiPool.rebalance | Council Lv6+ ≥4/7 multisig | Council-authorized DEX swap; swapRateBps within ±100 bps of Chainlink (stricter than per-tx ±50 bps band); councilAttestations minLength 4 |
| L7 | `jurisdictionAttestation` | (Council Lv7+ unanimity attestation flow) | `kawase_jurisdiction_compliance` cell | Per-jurisdiction Lv7+ unanimity activation gate (G14); councilAttestations minLength 5 (all Council seats); legalAnalysisCid = chigiri.ipLicenseClaim |
| L8 | `silenKawaseReview` | `kawase_silen_review` cell | Council Lv6+ ≥3 + toritate.annualReport | Quarterly aggregate audit; const-field structural enforcement of G3/G5/G7 |

## Schema Discipline (R0+)

- `additionalProperties: false` at top-level (Lexicon convention)
- `required` list covers every constitutionally-relevant field
- Stable enum `["USDC", "EURC", "JPYC", "KRWO", "GBPe", "CHFe"]` shared
  across L1/L2/L3 — R1 launch gates to USDC + EURC only; R2/R3 enable
  the rest with per-pair Council Lv7+ unanimity per L7
- L4 pair enum `["USD/EUR", "USD/JPY", "USD/KRW", "USD/GBP",
  "USD/CHF", "EUR/JPY", "EUR/GBP", "GBP/CHF"]` — R1 launch USD/EUR only
- L6 swap caps Solidity-enforced: swapAmount ≤10% of weaker pool;
  swapRate within ±100 bps of Chainlink
- L7 `councilAttestations` `minLength: 5` STRUCTURAL — all 5 Council
  seats must sign for jurisdiction activation (Council Lv7+ unanimity)
- L8 const-field structural enforcement:
  - `spreadProfitMkoto` const **0** (G5 — mid-market only)
  - `commercialRemittanceSoftwarePenetrationPct` const **0** (G7 —
    build-time enforced by
    `70-tools/scripts/lint/verify_no_commercial_remittance.py`)
  - `nonAdherentParticipationCount` const **0** (G3 — Solidity
    `onlyAdherent` modifier enforces at L6; this const is the
    audit-time mirror)

## R0 Status

Schemas at R0 carry the full const-field structural enforcement set.
R1 fills in `KawaseYuiPool.deposit()` / `claim()` / `rebalance()` Solidity
bodies + `kotoba_kawase.send()` / `claim()` Python bodies; the Lexicon
schemas themselves stay stable across R0 → R1.

Any addition / modification to any of the 8 Lexicons after R0 requires
the same Council attestation flow as the ADR: Lv6+ ≥3 for non-
constitutional fields, Lv7+ unanimity for any field that participates
in a const-0 / const-1 structural invariant.

## CI gates

- **`validate-lexicons.py`** — lefthook + GitHub Actions workflow
  (`.github/workflows/kawase-yui-r0-audit.yml` → `lexicon-schema-
  validation` lane). Fails if any of the 8 JSONs is malformed or
  drops the const-field structural enforcement.
- **`registry-schema-validation`** — lefthook hook validates the
  registry-side schema.

## Related Files

- `manifest.edn` — ActorManifest
- `README.md` — full inventory + 14 gates + R0→R3 ladder
- `/50-infra/etzhayyim-kawase-pool/src/KawaseYuiPool.sol` — L6 Solidity scaffold
- `/40-engine/kotoba_kawase/` — Python facade
- `/40-engine/kotoba/crates/kotoba-kotodama/cells/kawase_*/` — 5 R0 Pregel cell scaffolds
- `/70-tools/scripts/lint/verify_no_commercial_remittance.py` — G7
- `/90-docs/adr/2605282200-kawase-yui-multi-stable-adherent-remittance-mutual-aid.md` — Master ADR
- `/90-docs/adr/2605282100-kotoba-mkoto-economy-and-modal-billing-parity.md` — operator-side compute-cost layer
- `/90-docs/adr/2605263500-wakai-mutual-aid-tier-b-actor-r0.md` — sibling mutual-aid actor
