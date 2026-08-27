# kawase-yui (為替結) — Religious-Corp Multi-Stable Adherent Remittance Mutual-Aid Substrate

**DID**: `did:web:kawase-yui.etzhayyim.com`
**Namespace**: `com.etzhayyim.kawase.*`
**ADR**: ADR-2605282200 (R0 scaffold)
**Status**: R0 scaffold (2026-05-28) — 8 Lexicons + 5 Pregel cells + 1 Solidity scaffold + 1 Python facade + 1 build-time G7 lint hook
**Parent ADRs**: ADR-2605192100 (Mission Charter) + ADR-2605192200 (Charter Rider) + ADR-2605282100 (mKOTO economy)
**Sibling actor**: wakai (ADR-2605263500 — mutual aid framing precedent)
**Cross-actor**: chigiri (ADR-2605262700 — multi-jurisdiction + dispute mediation) + toritate (ADR-2605262900 — accounting)

## Overview

Religious-corp adherent-to-adherent multi-stable remittance built on the
pre-funded local-currency pool topology that TransferWise (Wise plc)
popularized — but re-framed under the constitutional constraints of
Charter §1.5 (anti-commercialization) + §2(b) (no speculative finance) +
ADR-2605282100 N2 (mKOTO non-transferability) + ADR-2605172100 Alt C (no
custom token).

Settlement uses **canonical Base L2 stablecoins** (USDC + EURC at R1;
+JPYC R2; +KRWO / +GBPe / +CHFe R3 with Council Lv7+ unanimity per
pair). Pool-match cell compute cost is billed in mKOTO via the
ADR-2605282100 economy. **No new token is minted.**

## Identity (CRITICAL)

- **NOT a commercial money-services business** (G14 + N1 + N5). No MSB
  / MTL / EMI / PI license sought. Structurally pinned to adherent
  mutual aid via the `onlyAdherent` Solidity modifier (G3 reverts
  `deposit()` + `claim()` when `AdherentRegistry.tokenOf(msg.sender) == 0`).
- **NOT proprietary FX trading or arbitrage** (N2). A bounded AMM may
  provide continuous stable-pair liquidity. Price impact, disclosed LP
  compensation and protocol revenue are accounted separately; operator-directed
  protocol fee is zero at R1 and can never exceed the contract ceiling.
- **NOT a fiat custodian** (N4 + G8). Religious-corp never holds fiat
  bank balances. Adherents on/off-ramp via their own exchange accounts;
  the pool only holds stablecoin ERC-20 positions.
- **NOT Travel-Rule / FATF passport KYC** (N8 + G10). Charter §1.12
  routing-around invariant; the Adherent SBT IS the KYC structurally.
- **NOT a chargeback system** (N9 + G11). On-chain finality; disputes
  route via chigiri.disputeMediation cooperative-first procedure
  (ADR-2605262700 G10 cross-actor).

## R0 inventory (landed 2026-05-28)

| Layer | Files | Tests |
|---|---|---|
| Lexicons (`lex/`) | 8 schemas (`depositAttestation` + `withdrawIntent` + `matchExecution` + `fxRateAttestation` + `poolStateReport` + `rebalanceAttestation` + `jurisdictionAttestation` + `silenKawaseReview`) | `validate-lexicons.py` 8/8 clean |
| Solidity (`50-infra/etzhayyim-kawase-pool/`) | policy + exact-input v4 adapter + fresh Chainlink cross-rate/sequencer gate + codehash-pinned registry/observer | 27/27 forge tests pass (policy + lifecycle + oracle freshness/round/sequencer + one-shot callback + pause/deadline/registry/fee refusal) |
| Python facade (`40-engine/kotoba_kawase/`) | `kotoba_kawase/__init__.py` + `kotoba_kawase/exceptions.py` (5 constitutional exceptions + KawaseError base) + `pyproject.toml` | 16/16 pytest pass (surface + R0 honesty + introspection + hierarchy + frozen dataclasses) |
| Pregel cells (`40-engine/kotoba/crates/kotoba-kotodama/cells/kawase_*/`) | 5 cells (`pool_match` + `fx_oracle_watcher` + `rebalance_proposer` + `jurisdiction_compliance` + `silen_review`) | each raises `RuntimeError` on import per kotodama R0 convention |
| Build-time lint (`70-tools/scripts/lint/`) | `verify_no_commercial_remittance.py` (G7) | 23/23 pytest pass; lefthook registered (`no-commercial-remittance`) |
| Constitution wiring (`50-infra/etzhayyim-chain-contracts/`) | `KAWASE_MAX_BAND_BPS` const + `KAWASE_PER_MONTH_CAP_USD_MINOR` mutable | `test_kawase_yui_constants_set` in religious-corp wave test |

## 14 immutable gates G1..G14

| Gate | Constitutional invariant | Enforcement |
|---|---|---|
| G1 | Charter Rider §2(a)-(h) scan on every memo + jurisdictionAttestation legalAnalysis + rebalanceAttestation justification | Charter Rider applicator (existing tooling) |
| G2 | kotoba attestation lineage MANDATORY | kotoba-datomic → kotoba per ADR-2605262130 |
| G3 | Adherent-SBT-gated deposit + claim | **Solidity-level** `onlyAdherent` modifier in `KawaseYuiPool.sol` |
| G4 | Mid-market Chainlink ±0.5% band | **Solidity-level** + **Constitution-level** const `KAWASE_MAX_BAND_BPS = 50` |
| G5 | No extractive or hidden protocol spread; LP compensation is disclosed separately | `protocolFeeBps` and `lpFeeBps` are distinct; R1 protocol fee = 0, hard cap = 5 bps, LP fee cap = 30 bps |
| G6 | Stable-only bounded AMM; no leverage, rehypothecation, arbitrary hooks or perp exposure | Oracle deviation + price-impact + min-out + liquidity checks in `validateAmmQuote`; approved adapter/hook codehash at R1 |
| G7 | NO commercial remittance MSB integration (Wise / Western Union / MoneyGram / Remitly / WorldRemit / Xoom / Revolut / OFX / Currencies Direct / Ria / Paysend / Atlantic Money / Sendwave / Boss Revolution / PayPal-Xoom / TransferWise) | **Build-time** `verify_no_commercial_remittance.py` lefthook gate |
| G8 | NO fiat custody | Pool contract is non-custodial; only stablecoin ERC-20 |
| G9 | Per-month USD-equivalent cap per member | **Constitution-level** mutable `KAWASE_PER_MONTH_CAP_USD_MINOR` |
| G10 | KYC = Adherent SBT (NO Travel Rule / FATF passport) | Charter §1.12 routing-around invariant |
| G11 | NO chargeback / NO fraud reversal | Pool contract has no `reverse()` / `unwind()` |
| G12 | Murakumo-only inference for all 5 cells | ADR-2605215000 fleet.toml allow-list (off-chain) |
| G13 | 100% kotoba content-addressed substrate | ADR-2605262130 invariant |
| G14 | Per-jurisdiction Council Lv7+ unanimity activation | **Pregel cell** `kawase_jurisdiction_compliance` (SOLE enforcement point — contract has no juris check) |

## Phase ladder R0 → R3

| Phase | Scope | State |
|---|---|---|
| **R0** | This commit — 8 Lexicons + 5 cells + Solidity scaffold + Python facade + G7 lint + Constitution wiring | **landed 2026-05-28** |
| **R1** | USDC↔EURC pair only / Chainlink USD-EUR feed / ≤50 adherents / ≤$50k aggregate pool / Council Lv6+ ≥3 ratify (RFP closes 2026-06-19) | gated on Bootstrap Council Seats 2-5 close |
| **R2** | +JPYC pair (Polygon-bridged via LayerZero with Council audit) / 30-day public objection / ≤500 adherents / ≤$500k aggregate / +`rebalance_proposer` + `jurisdiction_compliance` cells active | post-R1 |
| **R3** | +KRWO / +GBPe / +CHFe (per-pair Council Lv7+ unanimity) / ≤5,000 adherents / ≤$5M aggregate / +`silen_review` cell active / wakai cross-actor integration (medical-evacuation + cross-border bundle) | post-R2 |

## Why not just use Wise as a backend?

Constitutional barrier: Charter Rider §2(e) anti-gatekeeping + §2(c)
vendor data-sovereignty avoidance. Vendor closed query-tracking on
adherent financial posture is structurally unacceptable. The R0 G7
lint hook materializes this: any future commit that imports `wise` /
`remitly` / `moneygram` / `transferwise` / ... into a kawase runtime
path fails `lefthook` pre-commit.

## Why a constitutionally bounded AMM?

An AMM curve creates observable price impact; it does not by itself create
operator profit. LP compensation, protocol revenue and execution slippage are
different quantities and MUST remain separate in the ledger and UI. Kawase-yui
therefore permits constant-product or concentrated-liquidity adapters when the
pair is an approved stable pair and every execution satisfies the Chainlink
band, maximum price impact, participant `minAmountOut`, available-liquidity,
fee-cap, deadline and approved hook-codehash gates. Leverage,
rehypothecation, hidden routing and discretionary price overrides remain
unrepresentable. The reserve buffer remains a complementary circuit breaker,
not the sole constitutionally compatible topology.

## Cross-actor reverse-references

When the sibling actors land their R0+ work, they reference kawase-yui
as follows:

- **wakai** (ADR-2605263500) — `cross-actor: kawase-yui (international
  transfer; sibling mutual-aid framing)`
- **chigiri** (ADR-2605262700) — `cross-actor: kawase-yui
  (jurisdiction_compliance cell reads chigiri.ipLicenseClaim;
  disputeMediation handles kawase G11 disputes)`
- **toritate** (ADR-2605262900) — `cross-actor: kawase-yui
  (ledgerEntry purpose=kawase-mutual-aid; annual silenKawaseReview
  cross-references toritate.annualReport)`

## Migration Boundary

`src/kawase_yui/murakumo.cljc` is the current Murakumo-facing actor boundary for the
five legacy `kawase_*` kotoba-kotodama cells. It preserves the Python facade as an
R0 scaffold, but moves the domain actor contract into cljc data plans:

- `kawase_pool_match` -> `depositAttestation`, `withdrawIntent`, `matchExecution`
- `kawase_fx_oracle_watcher` -> `fxRateAttestation`
- `kawase_rebalance_proposer` -> `rebalanceAttestation`, `poolStateReport`
- `kawase_jurisdiction_compliance` -> `jurisdictionAttestation`
- `kawase_silen_review` -> `silenKawaseReview`

Every plan is blocked until Adherent-SBT, Chainlink mid-market band, zero-spread,
stable-only, no-commercial-remittance, no-fiat-custody, per-month-cap,
no-chargeback, Murakumo-only, kotoba-only, and Council Lv7 jurisdiction
attestations are present.

## Related ADRs / Files

- ADR-2608011200 — accepted bounded-AMM policy; supersedes ADR-2605282200 Alternative 8 and old G5/G6 wording
- ADR-2605282200 — kawase-yui charter (this actor's authoritative ADR)
- ADR-2605282100 — mKOTO economy (operator-side compute-cost layer)
- ADR-2605263500 — wakai mutual aid (sibling actor)
- ADR-2605262700 — chigiri legal procedure (multi-juris + dispute)
- ADR-2605262900 — toritate accounting (cross-actor ledger consumer)
- ADR-2605192130 — TitheRouter / 10% tithe (NOT applied at R0-R3 per §5 Kisha exemption)
- ADR-2605172100 — payments substrate (Base L2 + USDC + ERC-4337)
- `lex/` — 8 Lexicons
- `50-infra/etzhayyim-kawase-pool/` — Solidity L6
- `40-engine/kotoba_kawase/` — Python facade
- `40-engine/kotoba/crates/kotoba-kotodama/cells/kawase_*/` — 5 Pregel cells
- `70-tools/scripts/lint/verify_no_commercial_remittance.py` — G7
