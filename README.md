# DockSure

DockSure is a freight SLA escrow protocol, not a tracking-page classifier. A customer funds a shipment promise, the named carrier accepts it, and the carrier later submits public tracking, port, weather, or destination records. GenLayer validators independently re-fetch those sources and agree on one bounded verdict plus the exact evidence indexes supporting an exception. Deterministic code moves the escrow only after consensus.

## Lifecycle and settlement

1. `open_shipment` creates a unique lane agreement, locks native GEN, and binds two distinct customer-authorized HTTPS evidence origins before the carrier can act.
2. `accept_shipment` is restricted to the named carrier. Before acceptance, only the customer can cancel and recover escrow.
3. `submit_delivery` requires two distinct sources matching the customer's frozen policy. Every validator re-fetches the same records and agrees on their SHA-256 content digests as well as the bounded verdict.
4. `ON_TIME` and `EXCUSED` pay the carrier; `LATE` refunds the customer; `INSUFFICIENT` moves no funds and permits stronger evidence.
5. Carrier acceptance opens a 30-day evidence window. After it expires, `recover_unsettled` lets the customer recover escrow from an unresolved shipment without carrier cooperation.
6. Transfers emit only on `finalized`, after the appeal-sensitive consensus phase.

Evidence authorization parses HTTPS scheme, hostname, port and normalized path. Hostname-prefix tricks, encoded traversal, ambiguous overlapping slots and multiple records reusing one authorized slot are rejected before any web fetch.

The model never selects a recipient or amount. Evidence bodies are explicitly untrusted data. Expected, external, transient, and malformed-model errors are separated so validators cannot accidentally agree on unrelated failures.

## Product surface

The responsive operations desk supports wallet connection, funded shipment creation, carrier acceptance, evidence submission, receipt polling, contract reads, and a visible settlement manifest. All fields are editable; no workflow result is hardcoded.

## Verification

```bash
genvm-lint check contracts/contract.py
python -m pytest -q
```

The repository includes two transparent demo evidence records used for a real StudioNet lifecycle. Deployment metadata is in `deployment.json`.

## Deployment

- Contract: `0xCeBf663069290e2Db1086307e7c60c85280D2b12`
- Deploy tx: `0x843b4e167e1d0e9d4fa2dd3145d2f847996056f8f8c322e3e3d3cd70a6342f73`
- Reviewed source: `118f76b1ea5ed761233923145b77cb8b48f3939a`
- Live app: `https://docksure.pages.dev/`

## Proven StudioNet lifecycle

- Customer funding with two immutable authorized source slots: `0xb2671b4d4015aa79b63093b6c1021304c603368ae106ec4e0f9f63f2942c68a8`
- Named carrier acceptance from a different wallet: `0x02817f59cf2415cabf87f91642e0c1fc6cb06b09610a5b1ed33689249c66b603`
- Evidence consensus, two stored content digests and ON_TIME settlement: `0xaff53789902dbe055d6a1cf83c1d6b04a920f632f138b9aaaff5df5b5bb33755`

The verification script also requires hostname-prefix bypass and same-slot evidence simulations to fail before the positive settlement path runs. Direct behavioral regression tests cover both attacks, rejection of early recovery, and customer recovery after the 30-day deadline. The complete accepted run is recorded in `evidence/network-run.json`.
