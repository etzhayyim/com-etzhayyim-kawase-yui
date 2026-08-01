# ADR-2608011200: Kawase-yui permits a constitutionally bounded AMM

Status: accepted

Date: 2026-08-01

Supersedes: the AMM rejection in ADR-2605282200 Alternative 8 and its G5/G6 wording

## Decision

Kawase-yui permits constant-product and concentrated-liquidity AMM adapters for
approved stablecoin pairs. An AMM curve's price impact, liquidity-provider
compensation and protocol revenue are different quantities and must never be
collapsed into a single “spread profit” field.

R1 has these machine-enforced bounds:

- protocol fee: 0 bps by policy, immutable contract ceiling 5 bps;
- LP compensation: disclosed, maximum 30 bps;
- execution deviation from the fresh attested oracle: maximum 50 bps;
- participant `minAmountOut` and available output liquidity: mandatory;
- deadline, approved adapter codehash and approved hook codehash: mandatory in
  the R1 execution adapter;
- leverage, rehypothecation, arbitrary callbacks/hooks, hidden multi-DEX routing,
  discretionary price overrides and proprietary directional positions: forbidden.

The reserve buffer and counter-intent matcher remain useful complementary
liquidity sources. They are no longer described as the only constitutionally
compatible topology.

## Consequences

LPs may receive transparent compensation for capital and inventory risk without
that compensation being mislabeled as operator profit. Protocol revenue remains
zero at R1. Every circuit-breaker trip and the maximum observed price impact are
part of the quarterly `silenKawaseReview` evidence.

This ADR does not mint a new token and does not make mKOTO transferable.

## R0.1 adapter realization

The first Uniswap v4 realization is an exact-input, single-pool adapter. It
uses the PoolManager `unlock → swap → sync/settle → take` lifecycle with empty
`hookData`. Its immutable pool rejects dynamic fees and fees above 30 bps, and
it exposes no multicall, delegatecall or liquidity-management surface.

A Council-owned registry pins the reviewed runtime codehash for the adapter,
PoolManager and optional hook and provides a global pause. The R1 zero
protocol-fee value is an observation: because the external PoolManager can
change independently, an observer must pause execution when it detects a
mismatch. A designated observer has pause-only authority; only Council can
unpause or change approvals.

The adapter obtains its rate directly from a two-feed Chainlink cross-rate
oracle; callers cannot submit an oracle rate. Feed rounds must be complete,
positive, timestamp-valid, within their configured maximum age and retain their
reviewed decimals. On Base, execution also stops while the sequencer uptime feed
reports downtime and throughout the configured recovery grace period.

Deployment addresses, Base fork tests, Council ratification and an independent
security review remain deployment gates.

## R0.1 closure

R0.1 design and local verification are closed on 2026-08-01 with these
machine-enforced boundaries:

- the executor request contains no oracle-rate override;
- the immutable oracle derives both swap directions from two reviewed
  Chainlink feeds and emits the older observation timestamp;
- stale, non-positive, future-dated and incomplete rounds fail closed;
- a feed-decimals change fails closed instead of silently rescaling value;
- Base sequencer downtime and its nonzero post-recovery grace period fail
  closed;
- the v4 path is exact-input, single-pool and one-callback-only;
- adapter, PoolManager and optional hook runtime codehashes are pinned;
- a designated safety observer can only pause an approved pool mismatch;
  Council alone can unpause or change approvals;
- protocol fee, LP compensation and price impact remain separate evidence;
- settlement evidence records oracle contract/codehash, observation time and
  sequencer feed alongside execution and fee values.

The local closure evidence is 27 passing Forge tests, 37 passing canonical
actor tests, parseable EDN/JSON contracts and a clean whitespace diff check.
No contract was deployed, no token approval was granted and no funds moved.

R0.1 closure does not close R1. Mainnet feed and PoolManager addresses must be
ratified from current authoritative registries; the protocol-fee observer still
needs its production reader/keeper and operating key; Base fork tests, deploy
scripts, Council approval and independent security review remain mandatory.
